# app/__init__.py
from flask import Flask
from app.models import init_db
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    # Initialize the database
    init_db(app)
    
    # Register blueprints
    from app.routes.views import main
    app.register_blueprint(main)

    return app
