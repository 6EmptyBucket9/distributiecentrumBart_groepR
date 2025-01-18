from app.models import db
from app.models.ProductInBestelling import ProductInBestelling
from app.models.Product import Product

class ProductInBestellingController:

    @staticmethod
    def add_product_in_bestelling(bestelling, products_data):
        for productnr, data in products_data.items():
            product = Product.query.get(productnr)
            if product:
                product_in_bestelling = ProductInBestelling(
                    bestelling_id=bestelling.bestellingsnr,
                    product_id=product.productnr,
                    aantal=data['aantal'],
                    prijs=data['prijs']
                )
                db.session.add(product_in_bestelling)
        db.session.commit()

    @staticmethod
    def update_product_in_bestelling(bestelling, form_data):
        for key in form_data:
            if key.startswith('product_aantal_'):
                productnr = key.split('_')[-1]
                aantal = int(form_data[key])
                product_in_bestelling = ProductInBestelling.query.filter_by(
                    bestelling_id=bestelling.bestellingsnr,
                    product_id=productnr
                ).first()

                if product_in_bestelling:
                    product_in_bestelling.aantal = aantal
                else:
                    product = Product.query.get(productnr)
                    if product and aantal > 0:
                        new_product_in_bestelling = ProductInBestelling(
                            bestelling_id=bestelling.bestellingsnr,
                            product_id=product.productnr,
                            aantal=aantal,
                            prijs=float(form_data.get(f'product_prijs_{productnr}', 0))
                        )
                        db.session.add(new_product_in_bestelling)
        db.session.commit()

    @staticmethod
    def remove_product_in_bestelling(bestelling_id, product_id):
        product_in_bestelling = ProductInBestelling.query.filter_by(
            bestelling_id=bestelling_id,
            product_id=product_id
        ).first()

        if product_in_bestelling:
            db.session.delete(product_in_bestelling)
            db.session.commit()