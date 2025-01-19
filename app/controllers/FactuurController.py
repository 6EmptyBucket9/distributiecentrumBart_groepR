from app.models import db
from app.models.Factuur import Factuur
from app.models.Bestelling import Bestelling
from app.models.Klant import Klant
from datetime import datetime, timedelta

class FactuurController:

    @staticmethod
    def get_factuur_by_nr(factuurnr):
        """Fetch factuur by factuurnr (invoice number)."""
        return db.session.query(Factuur).filter_by(factuurnr=factuurnr).first()
    
    @staticmethod
    def get_factuur_by_klantnr(klantnr):
        """Fetch facturen by klantnr."""
        return db.session.query(Factuur).filter_by(factuur_klant=klantnr).first()


    @staticmethod
    def get_all_facturen():
        """Fetch all facturen."""
        return db.session.query(Factuur).all()

    @staticmethod
    def calculate_yearly_revenue(klantnr):
        """Calculate yearly revenue for a specific klant."""
        orders_last_year = (
            db.session.query(Factuur)
            .join(Bestelling, Factuur.factuur_bestelling == Bestelling.bestellingsnr)
            .filter(
                Factuur.factuur_klant == klantnr,
                Bestelling.datum >= (datetime.now() - timedelta(days=365))
            )
            .all()
        )

        yearly_revenue = sum(order.bestelling_rel.km_transport for order in orders_last_year)
        return yearly_revenue

    @staticmethod
    def calculate_customer_discount(yearly_revenue):
        """Calculate the customer discount based on yearly revenue."""
        if yearly_revenue < 10000:
            return 0.05  # 5% discount
        elif yearly_revenue >= 10000 and yearly_revenue < 20000:
            return 0.10  # 10% discount
        else:
            return 0.15  # 15% discount

    @staticmethod
    def calculate_total(factuur):
        """Calculate the final total including discounts."""
        klant = factuur.klant_rel
        yearly_revenue = FactuurController.calculate_yearly_revenue(klant.klantnr)
        klantkorting = FactuurController.calculate_customer_discount(yearly_revenue)
        
        factuur.klantkorting = klantkorting  # Store the calculated discount
        
        bestelling = factuur.bestelling_rel
        order_amount = bestelling.km_transport
        
        # Calculate order discount (5% for orders >= 500)
        order_discount = order_amount * 0.05 if order_amount >= 500 else 0
        
        # Calculate final amount after order discount and customer discount
        total_before_discount = order_amount - order_discount
        totaal_bedrag = total_before_discount - (total_before_discount * klantkorting)
        
        factuur.totaal_bedrag = totaal_bedrag  # Store the total amount in the factuur
        db.session.commit()  # Commit the changes to the database

    @staticmethod
    def update_factuur(factuurnr):
        """Update the factuur with calculated values."""
        factuur = FactuurController.get_factuur_by_nr(factuurnr)
        
        if not factuur:
            raise ValueError("Factuur not found")
        
        FactuurController.calculate_total(factuur)
        db.session.commit()  # Save the updated factuur

    @staticmethod
    def create_new_factuur(form_data):
        """Create a new factuur (invoice)."""
        new_factuur = Factuur(
            factuur_medewerker=form_data['factuur_medewerker'],
            factuur_klant=form_data['factuur_klant'],
            factuur_bestelling=form_data['factuur_bestelling'],
            datum_uitgifte=form_data['datum_uitgifte'],
            verval_datum=form_data['verval_datum'],
            betaling_status=form_data['betaling_status']
        )
        db.session.add(new_factuur)
        db.session.commit()

        FactuurController.calculate_total(new_factuur)  # Calculate and update the total and discount for the new invoice
        
        return new_factuur

    @staticmethod
    def get_related_models():
        """Fetch related models for creating/updating a factuur."""
        return {
            'klanten': db.session.query(Klant).all(),
            'bestellingen': db.session.query(Bestelling).all()
        }