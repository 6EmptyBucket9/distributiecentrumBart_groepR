from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import db 
from app.models.Bestelling import Bestelling

bestelling = Bestelling
main = Blueprint('main', __name__)

# Bestelling summary page
@main.route('/bestellingen', methods=['GET', 'POST'])
def show_orders():
    bestelling_status = request.form.get('status')
    bestelling_bestellingsnr = request.form.get('bestellingsnr')
   
    # Build the query dynamically
    query = db.session.query(Bestelling)
    if bestelling_status:
        query = query.filter(Bestelling.status == bestelling_status)
    if bestelling_bestellingsnr:
        query = query.filter(Bestelling.bestellingsnr == bestelling_bestellingsnr)

    bestellingen = query.all()

    return render_template('bestellingen.html', bestellingen=bestellingen, selected_status=bestelling_status)


@main.route('/bestelling/<int:bestelling_id>', methods=['GET', 'POST'])
def show_order_detail(bestelling_id):
    # Get bestelling by ID
    bestelling = db.session.query(Bestelling).filter_by(bestellingsnr=bestelling_id).first()

    if not bestelling:
        return jsonify({'error': 'Bestelling not found.'}), 404

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            # Update bestelling status
            bestelling_status = request.form.get('bestelling_status')
            if bestelling_status:
                bestelling.status = bestelling_status

            # Update products in bestelling
            for i, product_in_bestelling in enumerate(bestelling.products_in_bestelling):
                verschil_in_voorraad_value = request.form.get(f'products[{i}][verschil_in_voorraad]')
                aantal_value = request.form.get(f'products[{i}][aantal]')

                # Update verschil_in_voorraad if valid
                if verschil_in_voorraad_value and verschil_in_voorraad_value.isdigit():
                    product_in_bestelling.product_rel.verschil_in_voorraad = int(verschil_in_voorraad_value)

                # Update aantal if valid
                if aantal_value and aantal_value.isdigit():
                    product_in_bestelling.aantal = int(aantal_value)

            # Commit the changes to the database
            db.session.commit()

            # Redirect back to the detail page
            return redirect(url_for('main.show_orders', bestelling_id=bestelling_id))

    # Prepare products for rendering
    products = [
        {
            'productnr': product.productnr,
            'naam': product.naam,
            'voorraad': product.voorraad,
            'bederfelijkheidsfactor': product.bederfelijkheidsfactor,
            'batchnummer': product.batchnummer,
            'verpakkingsgrote': product.verpakkingsgrote,
            'locatie_id': product.locatie_id,
            'bewaaradvies': product.bewaaradvies,
            'product_fabrikant': product.product_fabrikant,
            'prijs': product_in_bestelling.prijs,
            'aantal': product_in_bestelling.aantal,
            'verschil_in_voorraad': product.verschil_in_voorraad,
            'locatie': product.locatie_rel.locatie_naam if product.locatie_rel else None,
            'bewaaradvies_naam': product.bewaaradvies_rel.advies if product.bewaaradvies_rel else None,
            'fabrikant_naam': product.fabrikant_rel.naam if product.fabrikant_rel else None,
        }
        for product_in_bestelling in bestelling.products_in_bestelling
        for product in [product_in_bestelling.product_rel]
    ]

    return render_template('bestelling_detail.html', bestelling=bestelling, products=products)

