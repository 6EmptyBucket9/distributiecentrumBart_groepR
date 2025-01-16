from app.models import db
from app.models.Levermoment import Levermoment

class LevermomentController:

    @staticmethod
    def get_all_levermomenten():
        """Get all levermomenten."""
        return db.session.query(Levermoment).all()
