import random
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
from app.controllers.KlantController import KlantController
main = Blueprint('main', __name__)

# Bestelling summary page
@main.route('/bestellingen', methods=['GET', 'POST'])
def show_orders():
    statuses = db.session.query(BestellingStatus).all()
    bestelling_status = request.form.get('status')
    bestelling_bestellingsnr = request.form.get('bestellingsnr')

    bestellingen = BestellingController.get_all_bestellingen()
    referrer = request.referrer
    if bestelling_status:
        bestellingen = BestellingController.get_bestelling_by_status(bestelling_status)
    if bestelling_bestellingsnr:
        bestellingen = BestellingController.get_bestelling_by_nr(bestelling_bestellingsnr)

    if isinstance(bestellingen, db.Query):
        bestellingen = bestellingen.all()

    # If bestellingen is a single Bestelling object, make it iterable by wrapping it in a list
    if isinstance(bestellingen, Bestelling):
        bestellingen = [bestellingen]

    return render_template('bestellingen_summary.html', bestellingen=bestellingen, statuses=statuses, selected_status=bestelling_status, referrer=referrer)

# Order detail page
@main.route('/bestelling/<int:bestelling_id>', methods=['GET', 'POST'])
def show_order_detail(bestelling_id):
    # Use the controller method to get bestelling by id
    bestelling = BestellingController.get_bestelling_by_nr(bestelling_id)
    statuses = BestellingStatusController.get_all_bestellingstatus()
    referrer = request.referrer
    if not bestelling:
        return jsonify({'error': 'Bestelling not found.'}), 404

    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            bestelling_status = request.form.get('status')  
            if bestelling_status:
                BestellingController.update_bestelling_status(bestelling, bestelling_status)

            ProductInBestellingController.update_product_in_bestelling(bestelling, request.form)

            return redirect(url_for('main.show_orders'))

    return render_template('bestelling_detail_orderpick.html', bestelling=bestelling, statuses=statuses, referrer=referrer)

# Order add page
@main.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        # Collect bestelling data
        form_data = {
            'bestelling_medewerker': request.form.get('bestelling_medewerker'),
            'datum': request.form.get('datum'),
            'status': request.form.get('status'),
            'bestelling_levermoment': request.form.get('bestelling_levermoment'),
            'bestelling_dagdeel': request.form.get('bestelling_dagdeel'),
            'bestelling_koerier': request.form.get('bestelling_koerier'),
            'km_transport': request.form.get('km_transport'),
            'spoed': request.form.get('spoed'),
        }

        # Collect and filter product data
        products_data = {}
        for key, value in request.form.items():
            if key.startswith('product_aantal_'):
                productnr = key.split('_')[-1]
                aantal = int(value)
                prijs = float(request.form.get(f'product_prijs_{productnr}', 0))
                
                # Only add products with aantal > 0
                if aantal > 0:
                    products_data[productnr] = {
                        'aantal': aantal,
                        'prijs': prijs,
                    }

        # Create bestelling
        new_bestelling = BestellingController.create_new_bestelling(form_data)

        # Add products to bestelling if any valid products exist
        if products_data:
            ProductInBestellingController.add_product_in_bestelling(new_bestelling, products_data)

        flash('Bestelling succesvol toegevoegd!', 'success')
        return redirect(url_for('main.show_orders'))

    # Get related models and products for the form
    related_models = BestellingController.get_related_models()
    products = ProductController.get_all_products()
    referrer = request.referrer

    return render_template('add_bestelling.html', related_models=related_models, products=products, referrer=referrer)


# Product summary page
@main.route('/products', methods=['GET', 'POST'])
def show_products():
    # Fetch all products using the controller method
    products = ProductController.get_all_products()
    locaties = LocatieController.get_all_locaties()
    fabrikanten = FabrikantController.get_all_fabrikanten()
    bewaaradviezen = BewaarAdviesController.get_all_bewaaradviezen()
    referrer = request.referrer
    # If no products are found, render the page with an empty list
    if not products:
        return render_template('producten.html', products=[], locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen,referrer=referrer)

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
# Product update page
@main.route('/product/update/<int:productnr>', methods=['GET', 'POST'])
def update_product(productnr):
    product = ProductController.get_product_by_nr(productnr)
    locaties = LocatieController.get_all_locaties()
    fabrikanten = FabrikantController.get_all_fabrikanten()
    bewaaradviezen = BewaarAdviesController.get_all_bewaaradviezen()
    referrer = request.referrer
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

    return render_template('update_product.html', product=product, locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen, referrer=referrer)

# Add product page
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    referrer = request.referrer
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

    return render_template('add_product.html', locaties=locaties, fabrikanten=fabrikanten, bewaaradviezen=bewaaradviezen, referrer=referrer)

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


# Fabrikant page
@main.route('/fabrikanten', methods=['GET', 'POST'])
def show_suppliers():
    referrer = request.referrer
    fabrikanten = FabrikantController.get_all_fabrikanten()

    if request.method == 'POST':
        naam = request.form.get('naam')
        emailadres = request.form.get('emailadres')
        telefoonnr = request.form.get('telefoonnr')

        if naam and emailadres and telefoonnr:
            FabrikantController.create_fabrikant(naam, emailadres, telefoonnr)
            flash('Fabrikant succesvol toegevoegd!', 'success')
        else:
            flash('Alle velden zijn verplicht.', 'danger')

        return redirect(url_for('main.show_suppliers'))

    return render_template('fabrikant_summary.html', fabrikanten=fabrikanten, referrer=referrer)
# Update fabrikant page
@main.route('/fabrikant/update/<int:idFabrikant>', methods=['GET', 'POST'])
def update_supplier(idFabrikant):
    referrer = request.referrer
    fabrikant = FabrikantController.get_fabrikant_by_id(idFabrikant)

    if not fabrikant:
        flash('Fabrikant niet gevonden.', 'danger')
        return redirect(url_for('main.show_suppliers'))  

    if request.method == 'POST':
        naam = request.form.get('naam')
        emailadres = request.form.get('emailadres')
        telefoonnr = request.form.get('telefoonnr')

        if naam and emailadres and telefoonnr:
            FabrikantController.update_fabrikant(idFabrikant, naam, emailadres, telefoonnr)
            flash('Fabrikant succesvol bijgewerkt!', 'success')
            return redirect(url_for('main.show_suppliers'))  
        else:
            flash('Alle velden zijn verplicht.', 'danger')

    return render_template('update_fabrikant.html', fabrikant=fabrikant, referrer=referrer)
# Add fabrikant page
@main.route('/fabrikant/add', methods=['GET', 'POST'])
def add_supplier():
    referrer = request.referrer
    if request.method == 'POST':
        # Collect form data
        naam = request.form.get('naam')
        emailadres = request.form.get('emailadres')
        telefoonnr = request.form.get('telefoonnr')

        # Validate inputs (optional but recommended)
        if not naam or not emailadres or not telefoonnr:
            flash("Alle velden zijn verplicht.", "warning")
            return redirect(url_for('main.add_supplier'))

        # Create a new supplier using the FabrikantController
        new_fabrikant = FabrikantController.create_fabrikant(naam, emailadres, telefoonnr)

        # Provide feedback and redirect to the supplier list
        if new_fabrikant:
            flash("Fabrikant succesvol toegevoegd.", "success")
        else:
            flash("Er is iets misgegaan. Probeer het opnieuw.", "danger")

        return redirect(url_for('main.show_suppliers'))

    return render_template('new_fabrikant.html', referrer=referrer)
# Dashboard page

@main.route('/dashboard')
def show_dashboard():

    out_of_stock = Product.query.filter(Product.voorraad == 0).all()
    soon_to_throw_away = random.randint(1, 100)  

    standard_transport = Bestelling.query.filter(Bestelling.spoed == 1).all()
    total_standard_km = sum([b.km_transport for b in standard_transport])


    emergency_transport = Bestelling.query.filter(Bestelling.spoed == 0).all()
    total_emergency_km = sum([b.km_transport for b in emergency_transport])


    co2_standard = total_standard_km * 0.25 
    co2_emergency = total_emergency_km * 0.30 

    return render_template(
        'dashboard.html',
        out_of_stock=out_of_stock,
        soon_to_throw_away=soon_to_throw_away,
        total_standard_km=total_standard_km,
        co2_standard=co2_standard,
        total_emergency_km=total_emergency_km,
        co2_emergency=co2_emergency
    )

# Klanten summary page
@main.route('/klanten', methods=['GET'])
def show_customers():
    referrer = request.referrer
    klanten = KlantController.get_all_klanten()
    return render_template('klanten_summary.html', klanten=klanten,referrer=referrer)

# Add Klant page
@main.route('/klant/add', methods=['GET', 'POST'])
def add_customer():
    referrer = request.referrer
    if request.method == 'POST':
        form_data = {
            'voornaam': request.form.get('voornaam'),
            'tussenvoegsel': request.form.get('tussenvoegsel'),
            'achternaam': request.form.get('achternaam'),
            'telefoonnr': request.form.get('telefoonnr')
        }
        new_klant = KlantController.create_klant(form_data)
        flash('Klant succesvol toegevoegd!', 'success')
        return redirect(url_for('main.show_customers'))

    return render_template('add_klant.html', referrer=referrer)

# Update Klant page
@main.route('/klant/update/<int:klantnr>', methods=['GET', 'POST'])
def update_customer(klantnr):
    referrer = request.referrer
    klant = KlantController.get_klant_by_id(klantnr)

    if request.method == 'POST':
        # Get the data from the form
        klant_data = {
            'voornaam': request.form.get('voornaam'),
            'tussenvoegsel': request.form.get('tussenvoegsel'),
            'achternaam': request.form.get('achternaam'),
            'email': request.form.get('email'),
            'telefoonnr': request.form.get('telefoonnr'),
        }

        KlantController.update_klant(klant, klant_data)

        flash('Klant succesvol bijgewerkt!', 'success')
        return redirect(url_for('main.show_customers', klantnr=klantnr,referrer=referrer)) 

    return render_template("update_klant.html", klant=klant)
