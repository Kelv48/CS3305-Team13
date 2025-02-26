# app/redis_listener.py
import redis
import json
import threading

def listen_to_channel():
    r = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe('activeSessions')  # Subscribe to the matchmaking server's channel
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            # Process data, for example, update game state or notify users
            print("Received message:", data)
            # You can add logic to update the Flask backend or trigger certain actions

def start_redis_listener():
    thread = threading.Thread(target=listen_to_channel)
    thread.daemon = True  # Daemon thread will exit when the main program exits
    thread.start()
