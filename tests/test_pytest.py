from app.controllers.ProductController import ProductController
from app.models.Product import Product
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


    