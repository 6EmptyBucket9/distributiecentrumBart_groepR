from sqlalchemy import Column, Integer, String
from app.models import db

class Klant(db.Model):
    __tablename__ = 'klant'

    klantnr = Column(Integer, primary_key=True)
    voornaam = Column(String(45), nullable=False)
    tussenvoegsel = Column(String(45), nullable=True)
    achternaam = Column(String(45), nullable=False)
    telefoonnr = Column(String(45), nullable=False)
<<<<<<< HEAD

 # Method to get a specific klant by klantnr
    @classmethod
    def get_klant(cls, klantnr):
        return cls.query.get(klantnr)  # This will return the klant object or None if not found

    # Method to delete a specific klant by klantnr
    @classmethod
    def delete_klant(cls, klantnr):
        klant = cls.query.get(klantnr)
        if klant:
            db.session.delete(klant)
            db.session.commit()
            return True
        return False

    # Optional: Method to get all klanten (if needed)
    @classmethod
    def get_all_klanten(cls):
        return cls.query.all()
=======
>>>>>>> a600c2dd2c98190fe8a1fb3b0e93f9e1daa916fd
