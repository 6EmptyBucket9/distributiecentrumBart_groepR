from flask import Blueprint, render_template
from app.models import db, get_reflected_model, reflect_product_in_bestelling

main = Blueprint('main', __name__)

@main.route('/bestelling/<int:bestelling_id>')
def show_products(bestelling_id):

    from app import create_app  # Lazy import to avoid circular import

    app = create_app()

    # Get reflected models dynamically
    Bestelling = get_reflected_model('bestelling')  
    Product = get_reflected_model('product')  
    # Reflect model manually cause its not found by base mapper
    Product_in_bestelling = reflect_product_in_bestelling(app.config['SQLALCHEMY_DATABASE_URI'])  # Reflect the 'product_in_bestelling' table

    # Query Bestelling table
    bestelling = db.session.query(Bestelling).filter_by(bestellingsnr=bestelling_id).first()

    if bestelling:
        result = db.session.execute(
            Product_in_bestelling.select().where(Product_in_bestelling.c.bestelling_bestellingsnr == bestelling_id)
        )
        
        products = []
        for record in result:
        
            product = db.session.query(Product).filter_by(productnr=record.product_productnr).first()
            if product:
                products.append(product)
      

        return render_template('bestelling_detail.html', bestelling=bestelling, products=products)

    return "Bestelling not found."
