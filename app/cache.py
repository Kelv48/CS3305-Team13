# app/cache.py
import redis
import json
from . import db
from .models import User, Stats, Leaderboard
from .models import User

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user_DBorCache(user_name):
    cache_key = f'user:{user_name}'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Cache hit")
        return json.loads(cached_data)
    
    print("Cache miss")
    user = User.query.filter_by(name=user_name).first()
    if user:
        user_data = {
            'id' : user.id,
            'name': user.name,
            'password' : user.password
        }

        redis_client.set(cache_key, json.dumps(user_data)) # Using setex to set an expiry time
        return user_data
    return None

def get_leaderboard():
    leaderboard_data = redis_client.get("leaderboard")
    
    if leaderboard_data:
        return json.loads(leaderboard_data)  # Convert JSON string to Python list
    
    # If no cached leaderboard, update it
    return update_leaderboard()

def update_leaderboard():
    try:
        stats_data = Stats.query.order_by(Stats.earnings.desc()).limit(10).all()

        if not stats_data:
            print("No data found in stats table.")
            return None  # Return None if no data exists

        leaderboard_list = []
        for stats in stats_data:
            leaderboard_entry = {
                "user_id": stats.user_id,
                "win_count": stats.win_count,
                "loss_count": stats.loss_count,
                "earnings": stats.earnings
            }
            leaderboard_list.append(leaderboard_entry)

            leaderboard_entry_db = Leaderboard.query.filter_by(stats_id=stats.id).first()
            if leaderboard_entry_db:
                leaderboard_entry_db.rank = leaderboard_list.index(leaderboard_entry) + 1
                leaderboard_entry_db.earnings = stats.earnings
            else:
                new_entry = Leaderboard(stats_id=stats.id, rank=leaderboard_list.index(leaderboard_entry) + 1, earnings=stats.earnings)
                db.session.add(new_entry)

        db.session.commit()

        redis_client.setex("leaderboard", 3600, json.dumps(leaderboard_list))

        return leaderboard_list
    except Exception as e:
        print(f"Error updating leaderboard: {e}")
        return None
