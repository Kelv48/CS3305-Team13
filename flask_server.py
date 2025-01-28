from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # to-do add a check to not allow duplicate names

    def __repr__(self):
        return f'<User {self.name}>'

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

@app.route("/user/<string:user_name>", methods=['GET'])
def get_user(user_name):
    user = get_user_DBorCache(user_name)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@app.route("/create_user", methods=['POST']) # add in a check for duplicate users to avoid errors
def create_user():
    data = request.json
    if not data.get('name') or not data.get('password'):
        return jsonify({'error': 'Please provide both name and password'}), 400
    new_user = User(name=data['name'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {data['name']} created successfully!", "id": new_user.id}), 201

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)