# app/routes.py
from flask import Blueprint, request, jsonify, g
from .models import User, Stats, Leaderboard
from .cache import get_user_DBorCache, get_leaderboard
from . import db
import json, redis, time

main = Blueprint('main', __name__)

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Route for user login
@main.route("/login", methods=['POST'])
def get_user():
    data = request.json
    
    # Check if the username and password are provided
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Please provide both username and password'}), 400

    # Fetch user data from cache or DB
    user = get_user_DBorCache(username)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# Route for user registration
@main.route("/register", methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Missing JSON in request'}), 400
    
    data = request.json

    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Please provide both username and password'}), 400
    
    # Check if the user already exists in cache or DB
    check = get_user_DBorCache(data['username'])
    if check:
        return jsonify({'error': 'User already exists'}), 400
    try:
        # Create new user and save to the database
        new_user = User(name=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        # Create the corresponding stats for the new user
        new_stats = Stats(user_id=new_user.id, win_count=0, loss_count=0, earnings=0)
        db.session.add(new_stats)
        db.session.commit()

        # Create a new leaderboard entry for the user
        new_leaderboard = Leaderboard(stats_id=new_stats.id, rank=0, earnings=0)
        db.session.add(new_leaderboard)
        db.session.commit()

        return jsonify({"message": f"User {data['username']} created successfully!", "id": new_user.id}), 201
    except Exception as e:
        return jsonify({"error": f"Error creating user: {str(e)}"}), 500

# Route for fetching the leaderboard
@main.route("/leaderboard", methods=['GET'])
def leaderboard():
    leaderboard_data = get_leaderboard()  # Call the function from cache to get the leaderboard

    if leaderboard_data:
        return jsonify(leaderboard_data), 200
    else:
        return jsonify({"error": "Leaderboard data not found"}), 404

# Route for user logout
@main.route("/logout", methods=['POST'])
def logout():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Please provide a username"}), 400
    user_session_key = f"user:{username}"
    if redis_client.exists(user_session_key):
        redis_client.delete(user_session_key)
        return jsonify({"message": f"User {username} logged out"}), 200
    return jsonify({"error": "User not found"}), 404

# Route for a basic test
@main.route('/')
def hello():
    return 'Hello, World!'

# Custom error handlers
@main.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404

@main.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal Server Error"}), 500
