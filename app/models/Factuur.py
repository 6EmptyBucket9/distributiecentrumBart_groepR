from sqlalchemy import Column, Integer, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.models import db
from app.models.Medewerker import Medewerker
from app.models.Klant import Klant
from app.models.Bestelling import Bestelling
from app.models.BetalingsStatus import BetalingsStatus
from datetime import datetime, timedelta 

class Factuur(db.Model):
    __tablename__ = 'factuur'

    factuurnr = Column(Integer, primary_key=True)
    factuur_medewerker = Column(Integer, ForeignKey('medewerker.Medewerkernr'), nullable=False)
    factuur_klant = Column(Integer, ForeignKey('klant.klantnr'), nullable=False)
    factuur_bestelling = Column(Integer, ForeignKey('bestelling.bestellingsnr'), nullable=False)
    datum_uitgifte = Column(Date, nullable=False)
    verval_datum = Column(Date, nullable=False)
    betaling_status = Column(Integer, ForeignKey('betalings_status.idBetalings_status'), nullable=False)

    medewerker_rel = db.relationship('Medewerker', backref='facturen')
    klant_rel = db.relationship('Klant', backref='facturen')
    bestelling_rel = db.relationship('Bestelling', backref='facturen')
    betalings_status_rel = db.relationship('BetalingsStatus', backref='facturen')


class Factuur(db.Model):
    __tablename__ = 'factuur'

    factuurnr = Column(Integer, primary_key=True)
    factuur_medewerker = Column(Integer, ForeignKey('medewerker.Medewerkernr'), nullable=False)
    factuur_klant = Column(Integer, ForeignKey('klant.klantnr'), nullable=False)
    factuur_bestelling = Column(Integer, ForeignKey('bestelling.bestellingsnr'), nullable=False)
    datum_uitgifte = Column(Date, nullable=False)
    verval_datum = Column(Date, nullable=False)
    betaling_status = Column(Integer, ForeignKey('betalings_status.idBetalings_status'), nullable=False)
    totaal_bedrag = Column(Numeric(10, 2), nullable=False)  # Total amount after all discounts
    klantkorting = Column(Numeric(5, 2), nullable=False)   # Customer discount based on yearly revenue

    medewerker_rel = db.relationship('Medewerker', backref='facturen')
    klant_rel = db.relationship('Klant', backref='facturen')
    bestelling_rel = db.relationship('Bestelling', backref='facturen')
    betalings_status_rel = db.relationship('BetalingsStatus', backref='facturen')

    # Method to calculate yearly revenue based on orders for the last year
    def calculate_yearly_revenue(self):
        klant = self.klant_rel
        # Query to calculate the total amount of orders in the past year
        orders_last_year = Bestelling.query.filter(
            Bestelling.bestelling_klant == klant.klantnr,
            Bestelling.datum >= (datetime.now() - timedelta(days=365))
        ).all()

        yearly_revenue = sum(order.km_transport for order in orders_last_year)
        return yearly_revenue

    # Method to calculate customer discount based on yearly revenue
    def calculate_customer_discount(self, yearly_revenue):
        if yearly_revenue < 10000:
            return 0.05  # 5% discount
        elif yearly_revenue >= 10000 and yearly_revenue < 20000:
            return 0.10  # 10% discount
        else:
            return 0.15  # 15% discount

    # Method to calculate the final amount
    def calculate_total(self):
        yearly_revenue = self.calculate_yearly_revenue()
        self.klantkorting = self.calculate_customer_discount(yearly_revenue)
        
        # Now calculate the discount for the order
        if self.bestelling_rel.km_transport >= 500:
            order_discount = self.bestelling_rel.km_transport * 0.05
        else:
            order_discount = 0
        
        # Calculate the final total amount considering both discounts
        total_before_discount = self.bestelling_rel.km_transport - order_discount
        self.totaal_bedrag = total_before_discount - (total_before_discount * self.klantkorting)