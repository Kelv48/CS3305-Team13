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
            'password' : user.password,
            'wallet' : user.wallet
        }

        redis_client.set(cache_key, json.dumps(user_data)) # Using setex to set an expiry time
        return user_data
    return None

def get_or_update_leaderboard():
    # Check if the leaderboard data exists in the cache
    leaderboard_data = redis_client.get("leaderboard")
    if leaderboard_data:
        print("Cache hit")
        return json.loads(leaderboard_data)  # Return cached leaderboard data
    
    print("Cache miss")
    try:
        # Fetch top-ranked players from the Stats table (sorted by earnings)
        stats_data = Stats.query.order_by(Stats.earnings.desc()).all()

        leaderboard_list = []
        last_earnings = None
        rank = 1

        # Process each player in stats_data and create leaderboard entries
        for i, stats in enumerate(stats_data):
            # Fetch the username from the User table using the user_id from Stats
            user = User.query.get(stats.user_id)
            if not user:
                continue  # Skip if user doesn't exist for some reason

            # If earnings have changed, update the rank
            if stats.earnings != last_earnings:
                rank = i + 1  # New rank for a new earnings value
            
            # Create a leaderboard entry
            leaderboard_entry = {
                "rank": rank,  # Rank is now the first value
                "username": user.name,  # Get the username of the user from the User table
                "win_count": stats.win_count,
                "loss_count": stats.loss_count,
                "earnings": stats.earnings
            }
            leaderboard_list.append(leaderboard_entry)

            last_earnings = stats.earnings

            # Update the Leaderboard table with the new rank and earnings
            leaderboard_entry_db = Leaderboard.query.filter_by(stats_id=stats.id).first()
            if leaderboard_entry_db:
                leaderboard_entry_db.rank = rank
                leaderboard_entry_db.earnings = stats.earnings
            else:
                new_entry = Leaderboard(stats_id=stats.id, rank=rank, earnings=stats.earnings)
                db.session.add(new_entry)

        # Commit changes to the database
        db.session.commit()

        # Store the updated leaderboard in Redis with a 1-hour expiry
        redis_client.setex("leaderboard", 3600, json.dumps(leaderboard_list))

        return leaderboard_list

    except Exception as e:
        print(f"Error updating leaderboard: {e}")
        return None