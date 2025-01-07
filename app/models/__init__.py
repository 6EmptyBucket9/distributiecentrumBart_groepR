# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData, Table

# Initialize db instance
db = SQLAlchemy()
Base = automap_base()

def init_db(app):
    """
    Initialize the db object for the app.
    """
    db.init_app(app)

def prepare_base(app):
    """
    Reflect the database schema into mapped classes using Automap.
    """
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # Reflect the entire database schema
    Base.prepare(engine, reflect=True)

def get_reflected_model(table_name):
    """
    Helper function to get the reflected model by table name.
    """
    return Base.classes.get(table_name)

# Function to reflect the 'product_in_bestelling' table manually
def reflect_product_in_bestelling(db_uri):
    engine = create_engine(db_uri)  # Use your actual database URI
    metadata = MetaData()

    # Reflect the 'product_in_bestelling' table
    product_in_bestelling = Table('product_in_bestelling', metadata, autoload_with=engine)

    # Print columns for verification
    print(product_in_bestelling.columns.keys())  # Lists column names of the reflected table

    return product_in_bestelling
