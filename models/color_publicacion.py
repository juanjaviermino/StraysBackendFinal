# models/color_publicacion.py
from utils.database import db  # Import the shared database instance
from .publicacion import Publicacion

class ColorPublicacion(db.Model):
    __tablename__ = 'ColorPublicacion'

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(10), nullable=False)
    publicacionId = db.Column(db.Integer, db.ForeignKey('Publicacion.publicacionId'), nullable=False)

    publicacion = db.relationship('Publicacion', backref=db.backref('colores', lazy=True))

    def __init__(self, color, publicacionId):
        self.color = color
        self.publicacionId = publicacionId

    # Additional methods and properties can be defined here
