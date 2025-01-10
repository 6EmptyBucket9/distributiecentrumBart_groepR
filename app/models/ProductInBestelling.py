from app.models import db  

class ProductInBestelling(db.Model):
    __tablename__ = 'product_in_bestelling' 

    bestelling_bestellingsnr = db.Column(db.Integer, primary_key=True)
    product_productnr = db.Column(db.Integer, primary_key=True)
    prijs = db.Column(db.Integer, nullable=False)
    aantal = db.Column(db.Integer, nullable=False)

    def __init__(self, bestelling_bestellingsnr, product_productnr, prijs, aantal):
        self.bestelling_bestellingsnr = bestelling_bestellingsnr
        self.product_productnr = product_productnr
        self.prijs = prijs
        self.aantal = aantal

    # Getters and Setters
    def get_bestelling_bestellingsnr(self):
        return self.bestelling_bestellingsnr

    def set_bestelling_bestellingsnr(self, new_bestelling_bestellingsnr):
        self.bestelling_bestellingsnr = new_bestelling_bestellingsnr

    def get_product_productnr(self):
        return self.product_productnr

    def set_product_productnr(self, new_product_productnr):
        self.product_productnr = new_product_productnr

    def get_prijs(self):
        return self.prijs

    def set_prijs(self, new_prijs):
        self.prijs = new_prijs

    def get_aantal(self):
        return self.aantal

    def set_aantal(self, new_aantal):
        self.aantal = new_aantal

    def __str__(self):
        return f'Bestelling Number: {self.bestelling_bestellingsnr}, Product Number: {self.product_productnr}, Price: {self.prijs}, Quantity: {self.aantal}'

    # Properties
    bestelling_bestellingsnr = property(get_bestelling_bestellingsnr, set_bestelling_bestellingsnr)
    product_productnr = property(get_product_productnr, set_product_productnr)
    prijs = property(get_prijs, set_prijs)
    aantal = property(get_aantal, set_aantal)
