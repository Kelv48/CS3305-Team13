# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load the config from a separate file
    app.config.from_object('app.config.Config')
    
    # Initialize the database and Redis client
    db.init_app(app)
    
    from .routes import main
    app.register_blueprint(main)
    
    return app