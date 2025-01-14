# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the database
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Register blueprints
    from app.routes.views import main
    app.register_blueprint(main, url_prefix='/')

    return app