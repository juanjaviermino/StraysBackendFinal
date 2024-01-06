# models/raza.py
from .especie import Especie
from utils.database import db  # Import the shared instance

class Raza(db.Model):
    __tablename__ = 'Raza'  # Updated to match the case in the new table definition

    id = db.Column(db.Integer, primary_key=True)
    raza = db.Column(db.String(100), nullable=False)  # Length updated to 100
    especieId = db.Column(db.Integer, db.ForeignKey('Especie.id'), nullable=False)  # Column name updated

    especie = db.relationship('Especie', backref=db.backref('razas', lazy=True))

    def __init__(self, raza, especieId):
        self.raza = raza
        self.especieId = especieId

    # Additional methods and properties can be defined here
