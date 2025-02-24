from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
# add an inbox to redis
# add game cache to redis
# ensure data is removed when appropriate

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # relationships
    stats = db.relationship('Stats', backref='user_statistics', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    win_count = db.Column(db.Integer, default=0, nullable=False, check=db.CheckConstraint('win_count >= 0'))
    loss_count = db.Column(db.Integer, default=0, nullable=False, check=db.CheckConstraint('loss_count >= 0'))
    earnings = db.Column(db.Integer, default=0, nullable=False, check=db.CheckConstraint('earnings >= 0'))

    # Relationships
    leaderboard = db.relationship('Leaderboard', backref='leaderboards', lazy=True, cascade="all, delete")

    @property
    def win_loss_ratio(self):
        if self.loss_count == 0 and self.win_count == 0:
            return None  # Both win and loss are zero, undefined ratio
        return self.win_count / self.loss_count if self.loss_count > 0 else float('inf')

    def __repr__(self):
        return f'<Stats {self.user_id}>'
    
class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id', ondelete='CASCADE'), unique=True, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    earnings = db.Column(db.Integer, default=0, nullable=False)
    
    __table_args__ = (db.UniqueConstraint('stats_id', name='unique_stats_leaderboard'),)

    def __repr__(self):
        return f'<Leaderboard {self.stats_id}>'


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

        redis_client.setex(cache_key, 300, json.dumps(user_data)) # Using setex to set an expiry time
        return user_data
    return None

@app.route("/user", methods=['POST'])
def get_user():
    data = request.json
    username = data.get('username')
    user = get_user_DBorCache(username)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@app.route("/create_user", methods=['POST']) 
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

# Run the application
if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True)