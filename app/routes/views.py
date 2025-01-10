from flask import Blueprint, render_template, request
from app.models import db 
from app.models.Bestelling import Bestelling

bestelling = Bestelling
main = Blueprint('main', __name__)

# Bestelling summary page
@main.route('/bestellingen', methods=['GET', 'POST'])
def show_filtered_orders():
    # Get bestelling status from form
    bestelling_status = request.form.get('status')
    # Check if status is status
    if bestelling_status:
        bestellingen = db.session.query(Bestelling).filter_by(status=bestelling_status).all()
    else:
        bestellingen = db.session.query(Bestelling).all()

    return render_template('bestellingen.html', bestellingen=bestellingen, selected_status=bestelling_status)

# Specific bestelling page
@main.route('/bestelling/<int:bestelling_id>', methods=['GET'])
def show_products_in_order(bestelling_id):
    # Get bestelling with bestelling_id
    bestelling = db.session.query(Bestelling).filter(Bestelling.bestellingsnr == bestelling_id).first()

    if not bestelling:
        return "Bestelling not found.", 404

    # Get the products with products in order
    products = []
    for product_in_bestelling in bestelling.products:
        product = product_in_bestelling.product_rel 
        product_data = {
            'product': product,
            'prijs': product_in_bestelling.prijs,
            'aantal': product_in_bestelling.aantal,
        }
        products.append(product_data) 

    return render_template('bestelling_detail.html', bestelling=bestelling, products=products)