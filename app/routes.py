# app/routes.py
from flask import Blueprint, request, jsonify
from .models import User
from .cache import get_user_DBorCache
from . import db
import json, redis

main = Blueprint('main', __name__)

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

@main.route("/login", methods=['POST'])
def get_user():
    data = request.json
    username = data.get('username')
    user = get_user_DBorCache(username)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@main.route("/register", methods=['POST'])
def create_user():
    data = request.json
    if not data.get('username') and data.get('password'):
        return jsonify({'error': 'Please provide both name and password'}), 400
    check = get_user_DBorCache(data['username'])
    if check:
        return jsonify({'error': 'User already exists'}), 400
    new_user = User(name=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {data['username']} created successfully!", "id": new_user.id}), 201

@main.route("/leaderboard", methods=['GET'])
def leaderboard():
    # Fetch leaderboard data from Redis
    leaderboard_data = redis_client.get("leaderboard")
    
    if leaderboard_data:
        # Convert JSON string to Python list
        return jsonify(json.loads(leaderboard_data)), 200
    else:
        return jsonify({"error": "Leaderboard data not found"}), 404
