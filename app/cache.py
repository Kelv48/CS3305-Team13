# app/cache.py
import redis
import json
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