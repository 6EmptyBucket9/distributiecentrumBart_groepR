from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from sqlalchemy.orm import joinedload
# model imports
from app.models import db 
from app.models.Bestelling import Bestelling
from app.models.BestellingStatus import BestellingStatus
from app.models.Product import Product
from app.models.Fabrikant import Fabrikant
from app.models.Locatie import Locatie
from app.models.BewaarAdvies import BewaarAdvies





main = Blueprint('main', __name__)

# Bestelling summary page
@main.route('/bestellingen', methods=['GET', 'POST'])
def show_orders():
    statuses = db.session.query(BestellingStatus).all()
    bestelling_status = request.form.get('status')
    bestelling_bestellingsnr = request.form.get('bestellingsnr')
    
    # Build the query dynamically
    query = db.session.query(Bestelling)
    if bestelling_status:
        query = query.filter(Bestelling.status == bestelling_status)
    if bestelling_bestellingsnr:
        query = query.filter(Bestelling.bestellingsnr == bestelling_bestellingsnr)

    bestellingen = query.all()

    return render_template('bestellingen.html', bestellingen=bestellingen, statuses=statuses, selected_status=bestelling_status)

# Order detail page
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

# Product summary page
@main.route('/producten', methods=['GET', 'POST'])
def show_products():
    # Fetch all products from the database along with their related data
    products = db.session.query(Product).all()

    # Fetch all locatie, fabrikant, and bewaaradvies objects from the database
    locaties = db.session.query(Locatie).all()
    fabrikanten = db.session.query(Fabrikant).all()
    bewaaradviezen = db.session.query(BewaarAdvies).all()

    # If no products are found, render the page with an empty list
    if not products:
        return render_template('producten.html', products=[], locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

    # Handle POST requests for form updates
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            # Process form data to update products using enumerate for the loop
            for i, product in enumerate(products):
                # Get input values from the form
                naam = request.form.get(f'products[{i}][naam]')
                voorraad = request.form.get(f'products[{i}][voorraad]')
                bederfelijkheidsfactor = request.form.get(f'products[{i}][bederfelijkheidsfactor]')
                batchnummer = request.form.get(f'products[{i}][batchnummer]')
                verpakkingsgrote = request.form.get(f'products[{i}][verpakkingsgrote]')
                locatie_id = request.form.get(f'products[{i}][locatie]')
                bewaaradvies_id = request.form.get(f'products[{i}][bewaaradvies]')
                fabrikant_id = request.form.get(f'products[{i}][fabrikant]')

                # Validate and update fields if valid data is provided
                if naam:
                    product.naam = naam
                if voorraad and voorraad.isdigit():
                    product.voorraad = int(voorraad)
                if bederfelijkheidsfactor and bederfelijkheidsfactor.isdigit():
                    product.bederfelijkheidsfactor = int(bederfelijkheidsfactor)
                if batchnummer:
                    product.batchnummer = batchnummer
                if verpakkingsgrote and verpakkingsgrote.isdigit():
                    product.verpakkingsgrote = int(verpakkingsgrote)
                if locatie_id:
                    product.locatie_id = int(locatie_id)  
                if bewaaradvies_id:
                    product.bewaaradvies = int(bewaaradvies_id)  
                if fabrikant_id:
                    product.product_fabrikant = int(fabrikant_id) 

            # commit changes to db
            db.session.commit()

            return redirect(url_for('main.show_products'))

    return render_template('producten.html', products=products, locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

# Add product page
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Extract data from the form
        naam = request.form['naam']
        bederfelijkheidsfactor = request.form['bederfelijkheidsfactor']
        batchnummer = request.form['batchnummer']
        verpakkingsgrote = request.form['verpakkingsgrote']
        voorraad = request.form['voorraad']
        locatie_id = request.form['locatie']
        bewaaradvies = request.form['bewaaradvies']
        product_fabrikant = request.form['fabrikant']

        # Create a new product instance and add it to the database
        new_product = Product(
            productnr = 0,
            naam=naam,
            bederfelijkheidsfactor=bederfelijkheidsfactor,
            batchnummer=batchnummer,
            verpakkingsgrote=verpakkingsgrote,
            voorraad=voorraad,
            verschil_in_voorraad=0,
            locatie_id=locatie_id,
            bewaaradvies=bewaaradvies,
            product_fabrikant=product_fabrikant
        )

        db.session.add(new_product)
        db.session.commit()

        # Redirect after adding the product
        return redirect(url_for('main.show_products'))  # Update with the correct route to show products

    # If GET, render the form and pass the needed data
    locaties = Locatie.query.all()
    fabrikanten = Fabrikant.query.all()
    bewaaradviezen = BewaarAdvies.query.all()

    return render_template('add_product.html', locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)




