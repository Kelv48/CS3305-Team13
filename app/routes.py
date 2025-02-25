# app/routes.py
from flask import Blueprint, request, jsonify
from .models import User, db, Stats, Leaderboard
from .cache import get_user_DBorCache
from . import db

main = Blueprint('main', __name__)

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
    leaderboard_data = (
        db.session.query(
            User.name.label("username"),
            Leaderboard.rank,
            Stats.win_count,
            Stats.loss_count,
            Stats.earnings
        )
        .join(Stats, User.id == Stats.user_id)  # Join User with Stats
        .join(Leaderboard, Stats.id == Leaderboard.stats_id)  # Join Stats with Leaderboard
        .order_by(Leaderboard.rank.asc())  # Sort by rank
        .all()
    )

    leaderboard_data = [
        {
            "username" : row.username,
            "rank" : row.rank,
            "wins" : row.win_count,
            "losses" : row.loss_count,
            "earnings" : row.earnings
        }
        for row in leaderboard_data
    ]
    return jsonify(leaderboard_data), 200