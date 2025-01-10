from flask import Blueprint, render_template, request
from app.models import db  # Import db from app
from app.models import get_reflected_model, reflect_product_in_bestelling
from app.models import Bestelling

bestelling = Bestelling
main = Blueprint('main', __name__)

# Order summary page
@main.route('/bestellingen', methods=['GET', 'POST'])
def show_filtered_orders():
    Bestelling = get_reflected_model('bestelling')  # Dynamically get the reflected model

    bestelling_status = request.form.get('status')

    if bestelling_status:
        bestellingen = db.session.query(Bestelling).filter_by(status=bestelling_status).all()
    else:
        bestellingen = db.session.query(Bestelling).all()

    return render_template('bestellingen.html', bestellingen=bestellingen, selected_status=bestelling_status)

# Example route for showing products in a specific order (bestelling)
@main.route('/bestelling/<int:bestelling_id>', methods=['GET'])
def show_products_in_order(bestelling_id):
    # Query the Bestelling by ID, and eager load the associated products
    bestelling = Bestelling.query.filter_by(bestellingsnr=bestelling_id).first()

    if not bestelling:
        return "Bestelling not found.", 404

    # Access the 'products' attribute to get the associated products in this bestelling
    products = []
    for product_in_bestelling in bestelling.products:
        product = product_in_bestelling.product  # This links to the Product table
        product_data = {
            'product': product,
            'prijs': product_in_bestelling.prijs,
            'aantal': product_in_bestelling.aantal,
        }
        products.append(product_data)

    return render_template('bestelling_detail.html', bestelling=bestelling, products=products)