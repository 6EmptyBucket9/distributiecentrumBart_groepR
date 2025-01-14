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
    return render_template('fabrikant_toevoegen.html')

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
    return render_template('rapport.html', omzet=omzet, totaal_bestellingen=totaal_bestellingen)

@main.route('/bestelling/details/<int:bestelling_id>', methods=['GET'])
def bestelling_details(bestelling_id):
    bestelling = Bestelling.query.get(bestelling_id)
    return render_template('bestelling_details.html', bestelling=bestelling)

@main.route('/bestelling/toevoegen', methods=['GET', 'POST'])
def new_bestelling():
    if request.method == 'POST':
        # Logic for adding a new order
        pass
    return render_template('new_bestelling.html')

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