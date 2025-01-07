# app/__init__.py
from flask import Flask
from app.models import init_db, prepare_base
from app.config import Config
def create_app():
    """
    Create and configure the app.
    """
    app = Flask(__name__)
    app.config.from_object(Config)  # Use your actual config here

    # Initialize the database
    init_db(app)
    
    # Prepare the base for reflection
    prepare_base(app)

    # Register the blueprint (ensure 'main' is imported later to avoid circular import)
    from app.routes.views import main
    app.register_blueprint(main)

    return app
