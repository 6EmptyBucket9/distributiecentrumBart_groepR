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
    # Reflect the database schema into models
    prepare_base(app)

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
    # Return the model class from the reflected base
    return Base.classes.get(table_name)

# Function to reflect the product_in_bestelling table manually
def reflect_product_in_bestelling(db_uri):
    """
    Manually reflect the 'product_in_bestelling' table as an SQLAlchemy Table.
    """
    engine = create_engine(db_uri) 
    metadata = MetaData()

    # Reflect the 'product_in_bestelling' table
    product_in_bestelling = Table('product_in_bestelling', metadata, autoload_with=engine)

    return product_in_bestelling
