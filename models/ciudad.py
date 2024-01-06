# models/ciudad.py
from utils.database import db  # Import the shared instance
from .provincia import Provincia

class Ciudad(db.Model):
    __tablename__ = 'Ciudad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    provinciaId = db.Column(db.Integer, db.ForeignKey('Provincia.id'), nullable=False)

    provincia = db.relationship('Provincia', backref=db.backref('ciudades', lazy=True))

    def __init__(self, nombre, provinciaId):
        self.nombre = nombre
        self.provinciaId = provinciaId

    # Additional methods and properties can be defined here
