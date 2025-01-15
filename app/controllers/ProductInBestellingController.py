from app.models import db
from app.models.ProductInBestelling import ProductInBestelling

class ProductInBestellingController:
    
    @staticmethod
    def add_product_in_bestelling(bestelling, products_data):
        """Add products to bestelling."""
        for productnr, data in products_data.items():
            product_in_bestelling = ProductInBestelling(
                bestelling_bestellingsnr=bestelling.bestellingsnr,
                product_productnr=productnr,
                aantal=data['aantal'],
                prijs=data['prijs']
            )
            db.session.add(product_in_bestelling)
        db.session.commit()

    @staticmethod
    def update_product_in_bestelling(bestelling, form_data):
        """Update products in bestelling."""
        for i, product_in_bestelling in enumerate(bestelling.products_in_bestelling):
            product_aantal = form_data.get(f'products[{i}][aantal]')
            if product_aantal and product_aantal.isdigit():
                product_in_bestelling.aantal = int(product_aantal)
            db.session.commit()