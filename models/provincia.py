# models/provincia.py
from utils.database import db  # Import the shared instance

class Provincia(db.Model):
    __tablename__ = 'Provincia'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    # Additional methods and properties can be defined here
