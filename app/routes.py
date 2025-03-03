from flask import Blueprint, request, jsonify, g
from .models import User, Stats, Leaderboard
from .cache import get_user_DBorCache, get_leaderboard
from . import db
import json, redis, time

main = Blueprint('main', __name__)

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

@main.route("/login", methods=['POST'])
def get_user():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Please provide both name and password'}), 400

    user = get_user_DBorCache(username)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@main.route("/register", methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Missing JSON in request'}), 400
    
    data = request.json

    if not data or not data.get('username') or data.get('password'):
        return jsonify({'error': 'Please provide both name and password'}), 400
    
    check = get_user_DBorCache(data['username'])
    if check:
        return jsonify({'error': 'User already exists'}), 400
    try:
        new_user = User(name=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        new_stats = Stats(user_id=new_user.id, win_count=0, loss_count=0, earnings=0)
        db.session.add(new_stats)
        db.session.commit()

        new_leaderboard = Leaderboard(stats_id=new_stats.id, rank=0, earnings=0)
        db.session.add(new_leaderboard)
        db.session.commit()

        return jsonify({"message": f"User {data['username']} created successfully!", "id": new_user.id}), 201
    except Exception as e:
        return jsonify({"error": "Error creating user"}), 500


@main.route("/leaderboard", methods=['GET'])
def leaderboard():
    leaderboard_data = get_leaderboard()  # Call the function from cache

    if leaderboard_data:
        return jsonify(leaderboard_data), 200
    else:
        return jsonify({"error": "Leaderboard data not found"}), 404

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
    
@main.route('/')
def hello():
    return 'Hello, World!'

@main.errorhandler(404)
def page_not_found(error):
    return "Page not found", 404

@main.errorhandler(500)
def internal_server_error(error):
    return "Internal Server Error", 500
