from sqlalchemy import Column, Integer, Date, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models import db
from app.models.Medewerker import Medewerker
from  app.models.BestellingStatus import BestellingStatus
from  app.models.Levermoment import Levermoment
from  app.models.Dagdeel import Dagdeel
from  app.models.Koerier import Koerier

class Bestelling(db.Model):
    __tablename__ = 'bestelling'
    bestellingsnr = Column(Integer, primary_key=True)
    bestelling_medewerker = Column(Integer, ForeignKey('medewerker.Medewerkernr'), nullable=False)
    datum = Column(Date, nullable=False)
    status = Column(Integer, ForeignKey('bestelling_status.idBestelling_status'), nullable=False)
    bestelling_levermoment = Column(Integer, ForeignKey('levermoment.idLevermoment'), nullable=False)
    bestelling_dagdeel = Column(Integer, ForeignKey('dagdeel.idDagdeel'), nullable=False)
    bestelling_koerier = Column(Integer, ForeignKey('koerier.idKoerier'), nullable=False)
    km_transport = Column(Integer, nullable=False)
    spoed = Column(SmallInteger, nullable=False)

    medewerker_rel = relationship('Medewerker', backref='bestellingen')
    status_rel = relationship('BestellingStatus', backref='bestellingen')
    levermoment_rel = relationship('Levermoment', backref='bestellingen')
    dagdeel_rel = relationship('Dagdeel', backref='bestellingen')
    koerier_rel = relationship('Koerier', backref='bestellingen')

    def get_bestellingsnr(self):
        return self.bestellingsnr

    def set_bestellingsnr(self, new_bestellingsnr):
        self.bestellingsnr = new_bestellingsnr

    bestellingsnr = property(get_bestellingsnr, set_bestellingsnr)
