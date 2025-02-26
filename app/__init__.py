from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .redis_listener import start_redis_listener

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load the config from a separate file
    app.config.from_object('app.config.Config')
    
    # Initialize the database
    db.init_app(app)
    migrate = Migrate(app, db)
    start_redis_listener()
    
    # Register the blueprint for routes
    from .routes import main
    app.register_blueprint(main)
    
    return app