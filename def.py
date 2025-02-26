import redis
import json

# Connect to Redis (modify host & port if necessary)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Default leaderboard data
default_leaderboard = [
    {"username": "Player1", "rank": 1, "wins": 10, "losses": 2, "earnings": 500},
    {"username": "Player2", "rank": 2, "wins": 8, "losses": 3, "earnings": 400},
    {"username": "Player3", "rank": 3, "wins": 6, "losses": 4, "earnings": 300},
]

# Save data in Redis
redis_client.set("leaderboard", json.dumps(default_leaderboard))

print("Default leaderboard data set in Redis!")