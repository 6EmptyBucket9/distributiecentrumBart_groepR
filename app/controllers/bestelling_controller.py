from flask import request
from app.models import db, get_reflected_model

class Bestelling_controller():
    def get_bestellingen():
        Bestelling = get_reflected_model('bestelling')  

        bestelling_status = request.form.get('status')

        if bestelling_status:
            print(bestelling_status)
            bestellingen = db.session.query(Bestelling).filter_by(status=bestelling_status).all()
        else:
            bestellingen = db.session.query(Bestelling).all()

        return bestellingen
