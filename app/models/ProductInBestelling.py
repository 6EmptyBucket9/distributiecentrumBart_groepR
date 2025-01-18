from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models import db
from app.models.Product import Product

class ProductInBestelling(db.Model):
    __tablename__ = 'product_in_bestelling'

    bestelling_bestellingsnr = Column(Integer, ForeignKey('bestelling.bestellingsnr'), primary_key=True)
    product_productnr = Column(Integer, ForeignKey('product.productnr'), primary_key=True)
    prijs = Column(Float, nullable=False)
    aantal = Column(Integer, nullable=False)

    product_rel = relationship("Product", backref='product_in_bestellingen')