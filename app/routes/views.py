from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
# model imports
from app.models import db 
from app.models.Bestelling import Bestelling
from app.models.BestellingStatus import BestellingStatus
from app.models.Product import Product
from app.models.Fabrikant import Fabrikant
from app.models.Locatie import Locatie
from app.models.BewaarAdvies import BewaarAdvies
from app.models.Medewerker import Medewerker
from app.models.Levermoment import Levermoment
from app.models.Dagdeel import Dagdeel
from app.models.Koerier import Koerier
from app.models.ProductInBestelling import ProductInBestelling
from app.models.BestellingStatus import BestellingStatus
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

    return render_template('bestellingen_summary.html', bestellingen=bestellingen, statuses=statuses, selected_status=bestelling_status)

# Order detail page
@main.route('/bestelling/<int:bestelling_id>', methods=['GET', 'POST'])
def show_order_detail(bestelling_id):
    # Get bestelling by ID
    bestelling = db.session.query(Bestelling).filter_by(bestellingsnr=bestelling_id).first()
    statuses = db.session.query(BestellingStatus).all()
    
    if not bestelling:
        return jsonify({'error': 'Bestelling not found.'}), 404

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            # Update bestelling status
            bestelling_status = request.form.get('status')  # Changed to 'status'
            if bestelling_status:
                bestelling.status = bestelling_status

            # Update products in bestelling using enumeration
            for i, product_in_bestelling in enumerate(bestelling.products_in_bestelling):
                verschil_in_voorraad_value = request.form.get(f'products[{i}][verschil_in_voorraad]')
                aantal_value = request.form.get(f'products[{i}][aantal]')

                # Validate and update the product details
                if verschil_in_voorraad_value and verschil_in_voorraad_value.isdigit():
                    product_in_bestelling.product_rel.verschil_in_voorraad = int(verschil_in_voorraad_value)

                if aantal_value and aantal_value.isdigit():
                    product_in_bestelling.aantal = int(aantal_value)

            db.session.commit()

            return redirect(url_for('main.show_orders'))

    return render_template('bestelling_detail_orderpick.html', bestelling=bestelling, statuses=statuses)

# Product summary page
@main.route('/products', methods=['GET', 'POST'])
def show_products():
    # Fetch all models
    products = db.session.query(Product).all()
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

    return render_template('product_summary.html', products=products, locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

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
        return redirect(url_for('main.show_products')) 
    # If GET, render the form and pass the needed data
    locaties = Locatie.query.all()
    fabrikanten = Fabrikant.query.all()
    bewaaradviezen = BewaarAdvies.query.all()

    return render_template('add_product.html', locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

# Add bestelling page
@main.route('/add_bestelling', methods=['GET', 'POST'])
def add_bestelling():
    # Fetch all models
    products = db.session.query(Product).all()
    medewerkers = db.session.query(Medewerker).all()
    koeriers = db.session.query(Koerier).all()
    levermomenten = db.session.query(Levermoment).all()
    dagdelen = db.session.query(Dagdeel).all()
    statuses = db.session.query(BestellingStatus).all()

    if request.method == 'POST':
        # Read the form data
        bestelling_medewerker = request.form.get('bestelling_medewerker')
        datum = request.form.get('datum')
        status = request.form.get('status')
        bestelling_levermoment = request.form.get('bestelling_levermoment')
        bestelling_dagdeel = request.form.get('bestelling_dagdeel')
        bestelling_koerier = request.form.get('bestelling_koerier')
        km_transport = request.form.get('km_transport')
        spoed = request.form.get('spoed')

        products_data = {}
        for product in products:
            # Fetch product quantities and prices from the form
            product_aantal = request.form.get(f'product_aantal_{product.productnr}', 0)
            product_prijs = request.form.get(f'product_prijs_{product.productnr}', 0)

            # Only include products with valid quantities and prices
            if int(product_aantal) > 0 and float(product_prijs) > 0:
                products_data[product.productnr] = {
                    'aantal': product_aantal,
                    'prijs': product_prijs
                }
            elif int(product_aantal) > 0 and float(product_prijs) > 0:
                print("fout")

        # Create new Bestelling object
        new_bestelling = Bestelling(
            bestelling_medewerker=bestelling_medewerker,
            datum=datum,
            status=status,
            bestelling_levermoment=bestelling_levermoment,
            bestelling_dagdeel=bestelling_dagdeel,
            bestelling_koerier=bestelling_koerier,
            km_transport=km_transport,
            spoed=spoed
        )

        try:
            # Add Bestelling to the database
            db.session.add(new_bestelling)
            db.session.commit()

            # Add ProductInBestelling entries
            for productnr, data in products_data.items():
                product_in_bestelling = ProductInBestelling(
                    bestelling_bestellingsnr=new_bestelling.bestellingsnr,
                    product_productnr=productnr,
                    aantal=data['aantal'],
                    prijs=data['prijs']
                )
            
                db.session.add(product_in_bestelling)

            db.session.commit()

            return redirect(url_for('main.show_orders', bestelling_id=new_bestelling.bestellingsnr))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while creating the bestelling: {str(e)}")
            return render_template('add_bestelling.html', products=products, medewerkers=medewerkers, koeriers=koeriers, levermomenten=levermomenten, dagdelen=dagdelen)

    # If GET request, render the form
    return render_template('add_bestelling.html', products=products, medewerkers=medewerkers, koeriers=koeriers, levermomenten=levermomenten, dagdelen=dagdelen, statuses=statuses)
