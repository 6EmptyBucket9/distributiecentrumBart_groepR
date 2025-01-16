# app/__init__.py
from flask import Flask
<<<<<<< HEAD
from flask_migrate import Migrate
from app.models import db
=======
from app.models import init_db
>>>>>>> a600c2dd2c98190fe8a1fb3b0e93f9e1daa916fd
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
<<<<<<< HEAD
    # Initialize the database
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Register blueprints
    from app.routes.views import main
    app.register_blueprint(main, url_prefix='/')

    return app
=======
    
    # Initialize the database
    init_db(app)
    
    # Register blueprints
    from app.routes.views import main
    app.register_blueprint(main)

    return app
>>>>>>> a600c2dd2c98190fe8a1fb3b0e93f9e1daa916fd
