from app.models import db
from app.models.Product import Product
from app.models.Locatie import Locatie
from app.models.Fabrikant import Fabrikant
from app.models.BewaarAdvies import BewaarAdvies
from sqlalchemy import and_
class ProductController:

    @staticmethod
    def create_product(form_data):
        """Create a new product from form data."""

        if any(char.isdigit() for char in form_data['naam']):
            return "Numbers in name is not allowed"
        new_product = Product(
            naam=form_data['naam'],
            bederfelijkheidsfactor=form_data['bederfelijkheidsfactor'],
            batchnummer=form_data['batchnummer'],
            verpakkingsgrote=form_data['verpakkingsgrote'],
            voorraad=form_data['voorraad'],
            verschil_in_voorraad=0, 
            locatie_id=form_data['locatie_id'],
            bewaaradvies=form_data['bewaaradvies'],
            product_fabrikant=form_data['fabrikant']
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def get_all_products():
        """Get all products."""
        return db.session.query(Product).all()

    @staticmethod
    def get_product_by_nr(productnr):
        """Get product by productnr."""
        return db.session.query(Product).filter_by(productnr=productnr).first()  # Return the first match or None

    @staticmethod
    def update_product(product, form_data):
        """Update an existing product."""
        product.naam = form_data['naam']
        product.bederfelijkheidsfactor = form_data['bederfelijkheidsfactor']
        product.batchnummer = form_data['batchnummer']
        product.verpakkingsgrote = form_data['verpakkingsgrote']
        product.voorraad = form_data['voorraad']
        product.locatie_id = form_data['locatie_id']
        product.bewaaradvies = form_data['bewaaradvies']
        product.product_fabrikant = form_data['fabrikant']

        db.session.commit()
        return product

    @staticmethod
    def delete_product(productnr):
        """Delete a product by productnr."""
        product_to_delete = db.session.query(Product).filter_by(productnr=productnr).first()
        if product_to_delete:
            db.session.delete(product_to_delete)
            db.session.commit()
        return product_to_delete
    
    @staticmethod
    def duplicate_product_entry(new_product):
        existing_product = (
            Product.query.filter(
                and_(
                    Product.naam == new_product.naam,
                    Product.bederfelijkheidsfactor == new_product.bederfelijkheidsfactor,
                    Product.batchnummer == new_product.batchnummer,
                    Product.verpakkingsgrote == new_product.verpakkingsgrote,
                    Product.voorraad == new_product.voorraad,
                    Product.verschil_in_voorraad == new_product.verschil_in_voorraad,
                    Product.locatie_id == new_product.locatie_id,
                    Product.bewaaradvies == new_product.bewaaradvies,
                    Product.product_fabrikant == new_product.product_fabrikant,
                )
            )
            .first()
        )
        return existing_product is not None