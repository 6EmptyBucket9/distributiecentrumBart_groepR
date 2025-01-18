from app.controllers.ProductController import ProductController
from app.models.Product import Product
from app.controllers.FactuurController import FactuurController
from app.models.Factuur import Factuur
from app.models.Bestelling import Bestelling
from app.models.Klant import Klant
from datetime import datetime, timedelta
from app.controllers.BestellingController import BestellingController
from app.controllers.ProductController import ProductController
from app.controllers.ProductInBestellingController import ProductInBestellingController
from app.models import db 
from app.models.BestellingStatus import BestellingStatus
from app.models.Product import Product
from app.controllers.FactuurController import FactuurController
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
from app import create_app 

def test_product_name():
    changed_product = Product(
        naam="Koolsla",
        bederfelijkheidsfactor=12,
        batchnummer=12,
        verpakkingsgrote=12,
        voorraad=12,
        verschil_in_voorraad=0, 
        locatie_id=1,
        bewaaradvies=1,
        product_fabrikant=1
    )

    assert not any(char.isdigit() for char in changed_product.naam), "Product name contains integers!"

def test_value_int_fields():
    changed_product = Product(
            naam="Koolsla",
            bederfelijkheidsfactor=12,
            batchnummer=1,
            verpakkingsgrote='12',
            voorraad=12,
            verschil_in_voorraad=0, 
            locatie_id=1,
            bewaaradvies=1,
            product_fabrikant=1
        )
    numeric_fields = {
        "bederfelijkheidsfactor": changed_product.bederfelijkheidsfactor,
        "batchnummer": changed_product.batchnummer,
        "verpakkingsgrote": changed_product.verpakkingsgrote,
        "voorraad": changed_product.voorraad,
        "verschil_in_voorraad": changed_product.verschil_in_voorraad,
        "locatie_id": changed_product.locatie_id,
        "bewaaradvies": changed_product.bewaaradvies,
        "product_fabrikant": changed_product.product_fabrikant,
    }

    for field_name, value in numeric_fields.items():
        assert isinstance(value, int), f"{field_name} is not an integer! Found: {type(value).__name__}"
 # Import your app factory function

def test_duplicate_product():

    app = create_app()  

    with app.app_context():
   
        new_product = Product(
            naam="Ham",
            bederfelijkheidsfactor=5,
            batchnummer=123,
            verpakkingsgrote=15,
            voorraad=18,
            verschil_in_voorraad=0, 
            locatie_id=3,
            bewaaradvies=3,
            product_fabrikant=2
        )

        is_duplicate = ProductController.duplicate_product_entry(new_product)

        assert not is_duplicate, "Duplicate product found in the database!"

def test_product_has_name():
    new_product = Product(
        naam=None, 
        bederfelijkheidsfactor=5,
        batchnummer=123,
        verpakkingsgrote=15,
        voorraad=18,
        verschil_in_voorraad=0, 
        locatie_id=3,
        bewaaradvies=3,
        product_fabrikant=2
    )

    assert new_product.naam, "Product name is missing or invalid!"


 #Test if yearly revenue is calculated correctly
def test_calculate_yearly_revenue():
    klant = Klant(klantnr=1, voornaam="John", tussenvoegsel="van", achternaam="Doe", telefoonnr="123456789")
    
    
    bestelling1 = Bestelling(bestellingsnr=1, bestelling_klant=klant.klantnr, km_transport=2000, datum=datetime.now() - timedelta(days=100))
    bestelling2 = Bestelling(bestellingsnr=2, bestelling_klant=klant.klantnr, km_transport=3000, datum=datetime.now() - timedelta(days=200))

    
    factuur = Factuur(factuur_klant=klant.klantnr)
    
    
    assert factuur.calculate_yearly_revenue() == 5000, f"Expected 5000, got {factuur.calculate_yearly_revenue()}"

# Test if the customer discount is calculated correctly based on yearly revenue for different amounts
def test_calculate_customer_discount():
    
    factuur_low = Factuur(factuur_klant=1)
    assert factuur_low.calculate_customer_discount(5000) == 0.05, "Expected 5% discount"

    
    factuur_medium = Factuur(factuur_klant=1)
    assert factuur_medium.calculate_customer_discount(15000) == 0.10, "Expected 10% discount"

    
    factuur_high = Factuur(factuur_klant=1)
    assert factuur_high.calculate_customer_discount(25000) == 0.15, "Expected 15% discount"

# Test if the total amount is calculated correctly based on order and discounts
def test_calculate_total():
    klant = Klant(klantnr=1, voornaam="John", tussenvoegsel="van", achternaam="Doe", telefoonnr="123456789")
    bestelling = Bestelling(bestellingsnr=1, bestelling_klant=klant.klantnr, km_transport=600, datum=datetime.now() - timedelta(days=10))

    factuur = Factuur(factuur_klant=klant.klantnr, bestelling_rel=bestelling)
    
   
    yearly_revenue = 10000
    factuur.calculate_total()  
    
    expected_discount = 0.10  
    expected_total = (600 - (600 * 0.05)) * (1 - expected_discount) 

  
    assert factuur.totaal_bedrag == expected_total, f"Expected total {expected_total}, got {factuur.totaal_bedrag}"
    assert factuur.klantkorting == expected_discount, f"Expected discount {expected_discount}, got {factuur.klantkorting}"
    

def test_show_orders():
    orders = BestellingController.get_all_bestellingen()
    assert orders is not None, "Failed to retrieve orders."

def test_order_detail():
    bestelling = BestellingController.get_bestelling_by_nr(1)
    assert bestelling is not None, "Order not found."

def test_add_order():
    form_data = {
        'bestelling_medewerker': 'Test Medewerker',
        'datum': '2024-01-01',
        'status': 'Nieuw',
        'bestelling_levermoment': 'Ochtend',
        'bestelling_dagdeel': 'Ochtend',
        'bestelling_koerier': 'Koerier 1',
        'km_transport': 10,
        'spoed': 0
    }
    new_order = BestellingController.create_new_bestelling(form_data)
    assert new_order is not None, "Failed to create a new order."

def test_show_products():
    products = ProductController.get_all_products()
    assert products is not None, "Failed to retrieve products."

def test_update_product():
    product = ProductController.get_product_by_nr(1)
    assert product is not None, "Product not found."
    updated_product = ProductController.update_product(product, {'voorraad': 20})
    assert updated_product.voorraad == 20, "Product update failed."

def test_add_product():
    form_data = {
        'naam': 'Test Product',
        'bederfelijkheidsfactor': 5,
        'batchnummer': 101,
        'verpakkingsgrote': 10,
        'voorraad': 100,
        'locatie_id': 1,
        'bewaaradvies': 1,
        'fabrikant': 1
    }
    new_product = ProductController.create_product(form_data)
    assert new_product is not None, "Failed to create a new product."

def test_show_suppliers():
    suppliers = FabrikantController.get_all_fabrikanten()
    assert suppliers is not None, "Failed to retrieve suppliers."

def test_add_supplier():
    new_supplier = FabrikantController.create_fabrikant("Test Supplier", "supplier@example.com", "1234567890")
    assert new_supplier is not None, "Failed to create a new supplier."

def test_update_supplier():
    fabrikant = FabrikantController.get_fabrikant_by_id(1)
    assert fabrikant is not None, "Supplier not found."
    FabrikantController.update_fabrikant(1, "Updated Supplier", "updated@example.com", "0987654321")
    updated_fabrikant = FabrikantController.get_fabrikant_by_id(1)
    assert updated_fabrikant.naam == "Updated Supplier", "Supplier update failed."

def test_show_customers():
    klanten = KlantController.get_all_klanten()
    assert klanten is not None, "Failed to retrieve customers."

def test_add_customer():
    form_data = {
        'voornaam': 'Test',
        'tussenvoegsel': '',
        'achternaam': 'User',
        'telefoonnr': '1234567890'
    }
    new_customer = KlantController.create_klant(form_data)
    assert new_customer is not None, "Failed to create a new customer."

def test_update_customer():
    klant = KlantController.get_klant_by_id(1)
    assert klant is not None, "Customer not found."
    KlantController.update_klant(klant, {'voornaam': 'Updated'})
    updated_klant = KlantController.get_klant_by_id(1)
    assert updated_klant.voornaam == 'Updated', "Customer update failed."

def test_dashboard():
    out_of_stock = Product.query.filter(Product.voorraad == 0).all()
    assert out_of_stock is not None, "Failed to retrieve out-of-stock products."

def test_factuur():
    factuur = FactuurController.get_factuur_by_nr(1)
    assert factuur is not None, "Invoice not found."
    FactuurController.update_factuur(1)
    updated_factuur = FactuurController.get_factuur_by_nr(1)
    assert updated_factuur is not None, "Invoice update failed."
