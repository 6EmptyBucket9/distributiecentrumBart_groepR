<<<<<<< HEAD
from flask import Flask, Blueprint, jsonify, request, render_template, redirect, url_for
from app.models import db  # Corrected import for db
from app.models.Bestelling import Bestelling  # Corrected import for Bestelling model
from app.models.Product import Product  # Corrected import for Product model
from app.models.Fabrikant import Fabrikant  # Corrected import for Fabrikant model
from app.models.Klant import Klant  # Corrected import for Klant model

main = Blueprint('main', __name__)

# ------------------ BACKEND FUNCTIONALITEITEN ------------------

# Homepagina met navigatie
@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# 1. Bestellingen beheren (CRUD)
@main.route('/bestellingen', methods=['GET', 'POST'])
def show_filtered_orders():
    bestelling_status = request.form.get('status')
    if bestelling_status:
        bestellingen = db.session.query(Bestelling).filter_by(status=bestelling_status).all()
    else:
        bestellingen = db.session.query(Bestelling).all()
    return render_template('bestellingen.html', bestellingen=bestellingen, selected_status=bestelling_status)

@main.route('/bestelling/<int:bestelling_id>', methods=['GET'])
def show_products_in_order(bestelling_id):
    bestelling = db.session.query(Bestelling).filter(Bestelling.bestellingsnr == bestelling_id).first()
    if not bestelling:
        return "Bestelling niet gevonden.", 404
    products = []
    for product_in_bestelling in bestelling.products:
        product = product_in_bestelling.product_rel
        products.append({
            'product': product,
            'prijs': product_in_bestelling.prijs,
            'aantal': product_in_bestelling.aantal,
        })
    return render_template('bestelling_detail.html', bestelling=bestelling, products=products)

@main.route('/bestelling/toevoegen', methods=['GET', 'POST'])
def new_bestelling():
    if request.method == 'POST':
        klantnr = request.form.get('klantnr')
        medewerker_id = request.form.get('medewerker_id')
        datum = request.form.get('datum')
        status = request.form.get('status')
        levermoment = request.form.get('levermoment')
        dagdeel = request.form.get('dagdeel')
        koerier = request.form.get('koerier')
        km_transport = request.form.get('km_transport')
        spoed = request.form.get('spoed')

        nieuwe_bestelling = Bestelling(
            klantnr=klantnr,
            bestelling_medewerker=medewerker_id,
            datum=datum,
            status=status,
            bestelling_levermoment=levermoment,
            bestelling_dagdeel=dagdeel,
            bestelling_koerier=koerier,
            km_transport=km_transport,
            spoed=spoed
        )
        db.session.add(nieuwe_bestelling)
        db.session.commit()
        return redirect(url_for('main.show_filtered_orders'))

    klanten = Klant.query.all()
    return render_template('new_bestelling.html', klanten=klanten)

# 2. Fabrikanten beheren
@main.route('/fabrikanten', methods=['GET'])
def get_fabrikanten():
    fabrikanten = Fabrikant.query.all()
    return render_template('fabrikanten.html', fabrikanten=fabrikanten)

@main.route('/fabrikant/toevoegen', methods=['GET', 'POST'])
def voeg_fabrikant_toe():
    if request.method == 'POST':
        data = request.form
        nieuwe_fabrikant = Fabrikant(naam=data['naam'], emailadres=data['emailadres'], telefoonnr=data['telefoonnr'])
        db.session.add(nieuwe_fabrikant)
        db.session.commit()
        return redirect(url_for('main.get_fabrikanten'))
    return render_template('new_supplier.html')

# 3. Betalingsstatus bekijken
@main.route('/betalingen', methods=['GET'])
def get_betalingsstatus():
    bestellingen = Bestelling.query.all()
    return render_template('betalingen.html', bestellingen=bestellingen)

# 4. Klantinformatie beheren
@main.route('/klanten', methods=['GET'])
def get_klanten():
    klanten = Klant.query.all()
    return render_template('klanten.html', klanten=klanten)

@main.route('/klanten')
def klanten():
    # Fetch all klanten from the database
    klanten = Klant.get_all_klanten()
    return render_template('klanten.html', klanten=klanten)

@main.route('/klant/bewerken/<int:klantnr>', methods=['GET', 'POST'])
def bewerken_klant(klantnr):
    klant = Klant.get_klant(klantnr)
    if klant:
        # Handle editing the klant (example: update form)
        if request.method == 'POST':
            # Update klant data here
            pass
        return render_template('bewerken_klant.html', klant=klant)
    else:
        # Return error or redirect if klant is not found
        return redirect(url_for('main.klanten'))

@main.route('/klant/verwijderen/<int:klantnr>', methods=['POST'])
def verwijderen_klant(klantnr):
    success = Klant.delete_klant(klantnr)
    if success:
        # Redirect to klanten overview page
        return redirect(url_for('main.klanten'))
    else:
        # Handle error case (e.g., klant not found)
        return redirect(url_for('main.klanten'))

# 5. Financiële rapporten genereren
@main.route('/rapport', methods=['GET'])
def genereer_rapport():
    omzet = db.session.query(db.func.sum(Bestelling.totaalbedrag)).scalar()
    totaal_bestellingen = Bestelling.query.count()

    # Fetch the first klant (customer) for the report or pass None if not available
    klant = Klant.query.first()  # Or another logic to fetch the right klant

    # Check if klant is found and pass it to the template
    return render_template(
        'rapport.html',
        klant=klant,  # Make sure 'klant' is passed to the template
        omzet=omzet,
        totaal_bestellingen=totaal_bestellingen
    )
@main.route('/bestelling/details/<int:bestelling_id>', methods=['GET'])
def bestelling_details(bestelling_id):
    bestelling = Bestelling.query.get(bestelling_id)
    return render_template('bestelling_details.html', bestelling=bestelling)

@main.route('/product/toevoegen', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        # Logic for adding a new product
        pass
    return render_template('new_product.html')

@main.route('/supplier/toevoegen', methods=['GET', 'POST'])
def new_supplier():
    if request.method == 'POST':
        # Logic for adding a new supplier
        pass
    return render_template('new_supplier.html')

@main.route('/financieel_rapport/<int:klantnr>')
def financieel_rapport(klantnr):
    # Fetch klant (customer) by klantnr
    klant = Klant.query.get_or_404(klantnr)

    # Calculate total omzet (revenue)
    total_revenue = db.session.query(db.func.sum(Bestelling.totaalbedrag)) \
        .filter(Bestelling.klantnr == klantnr).scalar() or 0

    # Calculate total number of bestellingen (orders)
    total_orders = Bestelling.query.filter_by(klantnr=klantnr).count()

    # Fetch past transactions (bestellingen) for the klant
    transactions = Bestelling.query.filter_by(klantnr=klantnr).all()

    # Pass the data (klant, omzet, total_orders, transactions) to the template
    return render_template(
        'rapport.html',
        klant=klant,  # Pass klant here
        omzet=total_revenue,
        totaal_bestellingen=total_orders,
        transactions=transactions
    )

=======
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
# model imports
from app.controllers.BestellingController import BestellingController
from app.controllers.ProductController import ProductController
from app.controllers.ProductInBestellingController import ProductInBestellingController
from app.models import db 
from app.models.BestellingStatus import BestellingStatus
from app.models.Product import Product
from app.models.Fabrikant import Fabrikant
from app.models.Locatie import Locatie
from app.models.BewaarAdvies import BewaarAdvies
from app.controllers.BestellingController import BestellingController
from app.controllers.BewaarAdviesController import BewaarAdviesController
from app.controllers.LocatieController import LocatieController
from app.controllers.BestellingStatusController import BestellingStatusController
from app.models.Bestelling import Bestelling
from app.controllers.FabrikantController import FabrikantController
from app.controllers.DagDeelController import DagdeelController
from app.controllers.LevermomentController import LevermomentController
from app.controllers.KoerierController import KoerierController
from app.controllers.MedewerkersController import MedewerkerController
main = Blueprint('main', __name__)

# Bestelling summary page
@main.route('/bestellingen', methods=['GET', 'POST'])
def show_orders():
    statuses = db.session.query(BestellingStatus).all()
    bestelling_status = request.form.get('status')
    bestelling_bestellingsnr = request.form.get('bestellingsnr')

    bestellingen = BestellingController.get_all_bestellingen()

    if bestelling_status:
        bestellingen = BestellingController.get_bestelling_by_status(bestelling_status)
    if bestelling_bestellingsnr:
        bestellingen = BestellingController.get_bestelling_by_nr(bestelling_bestellingsnr)

    if isinstance(bestellingen, db.Query):
        bestellingen = bestellingen.all()

    # If bestellingen is a single Bestelling object, make it iterable by wrapping it in a list
    if isinstance(bestellingen, Bestelling):
        bestellingen = [bestellingen]

    return render_template('bestellingen_summary.html', bestellingen=bestellingen, statuses=statuses, selected_status=bestelling_status)

# Order detail page
@main.route('/bestelling/<int:bestelling_id>', methods=['GET', 'POST'])
def show_order_detail(bestelling_id):
    # Use the controller method to get bestelling by id
    bestelling = BestellingController.get_bestelling_by_nr(bestelling_id)
    statuses = BestellingStatusController.get_all_bestellingstatus()
    
    if not bestelling:
        return jsonify({'error': 'Bestelling not found.'}), 404

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            bestelling_status = request.form.get('status')  
            if bestelling_status:
                BestellingController.update_bestelling_status(bestelling, bestelling_status)

            ProductInBestellingController.update_product_in_bestelling(bestelling, request.form)

            return redirect(url_for('main.show_orders'))

    return render_template('bestelling_detail_orderpick.html', bestelling=bestelling, statuses=statuses)

# Product summary page
@main.route('/products', methods=['GET', 'POST'])
def show_products():
    # Fetch all products using the controller method
    products = ProductController.get_all_products()
    locaties = LocatieController.get_all_locaties()
    fabrikanten = FabrikantController.get_all_fabrikanten()
    bewaaradviezen = BewaarAdviesController.get_all_bewaaradviezen()

    # If no products are found, render the page with an empty list
    if not products:
        return render_template('producten.html', products=[], locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

    # Handle POST requests for form updates
    if request.method == 'POST':
        # Debugging: Print the entire form data to understand its structure
        print("Request Form Data:", request.form)

        if request.form.get('_method') == 'PUT':
            # Extract product data from the form
            product_updates = {}
            for key in request.form:
                if key.startswith('products'):
                    # Extract index from the form key (e.g., 'products[0][naam]')
                    index = int(key.split('[')[1].split(']')[0])
                    field_name = key.split('[')[2].split(']')[0]

                    if index not in product_updates:
                        product_updates[index] = {}

                    # Update the product dictionary with the field value
                    product_updates[index][field_name] = request.form[key]

            for index, product_data in product_updates.items():
                productnr = product_data.get('productnr')
                if productnr:
                    product = Product.query.get(productnr)
                    if product:
                        # Update the product using the ProductController
                        updated_product = ProductController.update_product(product, {
                            'naam': product_data.get('naam'),
                            'voorraad': product_data.get('voorraad'),
                            'bederfelijkheidsfactor': product_data.get('bederfelijkheidsfactor'),
                            'batchnummer': product_data.get('batchnummer'),
                            'verpakkingsgrote': product_data.get('verpakkingsgrote'),
                            'locatie_id': product_data.get('locatie'),
                            'fabrikant': product_data.get('fabrikant'),
                            'bewaaradvies': product_data.get('bewaaradvies')
                        })
                        print(f"Updated product: {updated_product}")
                    else:
                        print(f"Product with number {productnr} not found.")
                else:
                    print(f"No 'id' found for product {index}")

            return redirect(url_for('main.show_products'))

    return render_template('product_summary.html', products=products, locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

@main.route('/product/update/<int:productnr>', methods=['GET', 'POST'])
def update_product(productnr):
    product = ProductController.get_product_by_nr(productnr)
    locaties = LocatieController.get_all_locaties()
    fabrikanten = FabrikantController.get_all_fabrikanten()
    bewaaradviezen = BewaarAdviesController.get_all_bewaaradviezen()

    if request.method == 'POST':
        form_data = {
            'naam': request.form['naam'],
            'voorraad': request.form['voorraad'],
            'bederfelijkheidsfactor': request.form['bederfelijkheidsfactor'],
            'batchnummer': request.form['batchnummer'],
            'verpakkingsgrote': request.form['verpakkingsgrote'],
            'locatie_id': request.form['locatie_id'],
            'bewaaradvies': request.form['bewaaradvies_id'],
            'fabrikant': request.form['fabrikant_id'] 
        }
        
        updated_product = ProductController.update_product(product, form_data)
        db.session.commit()
        return redirect(url_for('main.show_products'))

    return render_template('update_product.html', product=product, locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

# Add product page
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        form_data = {
            'naam': request.form['naam'],
            'bederfelijkheidsfactor': request.form['bederfelijkheidsfactor'],
            'batchnummer': request.form['batchnummer'],
            'verpakkingsgrote': request.form['verpakkingsgrote'],
            'voorraad': request.form['voorraad'],
            'locatie_id': request.form['locatie'], 
            'bewaaradvies': request.form['bewaaradvies'],  
            'fabrikant': request.form['fabrikant']  
        }

        new_product = ProductController.create_product(form_data)

        return redirect(url_for('main.show_products'))

    locaties = Locatie.query.all()
    fabrikanten = Fabrikant.query.all()
    bewaaradviezen = BewaarAdvies.query.all()

    return render_template('add_product.html', locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen)

# Add bestelling page
@main.route('/add_bestelling', methods=['GET', 'POST'])
def add_bestelling():
    # Fetch all models
    products = ProductController.get_all_products()
    medewerkers = MedewerkerController.get_all_medewerkers()
    koeriers = KoerierController.get_all_koeriers()
    levermomenten = LevermomentController.get_all_levermomenten
    dagdelen = DagdeelController.get_all_dagdelen()
    statuses = db.session.query(BestellingStatus).all()

    if request.method == 'POST':
        # Read the form data
        form_data = {
            'bestelling_medewerker': request.form.get('bestelling_medewerker'),
            'datum': request.form.get('datum'),
            'status': request.form.get('status'),
            'bestelling_levermoment': request.form.get('bestelling_levermoment'),
            'bestelling_dagdeel': request.form.get('bestelling_dagdeel'),
            'bestelling_koerier': request.form.get('bestelling_koerier'),
            'km_transport': request.form.get('km_transport'),
            'spoed': request.form.get('spoed')
        }

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

        # Create new Bestelling using the controller
        new_bestelling = BestellingController.create_new_bestelling(form_data)

        # Add ProductInBestelling entries
        BestellingController.add_product_in_bestelling(new_bestelling, products_data)

        return redirect(url_for('main.show_orders', bestelling_id=new_bestelling.bestellingsnr))
    return render_template('add_bestelling.html', products=products, medewerkers=medewerkers, koeriers=koeriers, levermomenten=levermomenten, dagdelen=dagdelen, statuses=statuses)


# Track and trace page
@main.route('/track_trace', methods=['GET', 'POST'])
def track_and_trace():
    statuses = BestellingStatusController.get_all_bestellingstatus()
    levermomenten = LevermomentController.get_all_levermomenten()
    dagdelen = DagdeelController.get_all_dagdelen()
    bestelling = None
    track_code = None
    bestelling_bestellingsnr = request.form.get('bestellingsnr')  

    if request.method == 'POST' and not request.form.get('_method'):
        if 'bestellingsnr' in session:
            session.pop('bestellingsnr', None)

        if bestelling_bestellingsnr:
            bestelling = BestellingController.get_bestelling_by_nr(bestelling_bestellingsnr)
            session['bestellingsnr'] = bestelling.bestellingsnr if bestelling else None
            track_code = BestellingController.generate_track_code()

            if not bestelling:
                return redirect(url_for('main.track_and_trace'))

    if 'bestellingsnr' in session:
        bestelling = BestellingController.get_bestelling_by_nr(session['bestellingsnr'])
    
    if request.method == 'POST' and request.form.get('_method') == 'PUT':
        if bestelling:  
            # Get form values to update
            bestelling_status = request.form.get('status')
            bestelling_levermoment = request.form.get('bestelling_levermoment')
            bestelling_dagdeel = request.form.get('bestelling_dagdeel')
            
            # Update bestelling fields using the controller method
            BestellingController.update_bestelling_status(bestelling, bestelling_status)
            BestellingController.update_bestelling_levermoment(bestelling, bestelling_levermoment)
            BestellingController.update_bestelling_dagdeel(bestelling, bestelling_dagdeel)

            db.session.commit()
            session.pop('bestellingsnr', None)
            return redirect(url_for('main.track_and_trace')) 

    return render_template('track_trace.html', bestelling=bestelling, levermomenten=levermomenten, dagdelen=dagdelen, statuses=statuses, track_code=track_code)
>>>>>>> a600c2dd2c98190fe8a1fb3b0e93f9e1daa916fd
