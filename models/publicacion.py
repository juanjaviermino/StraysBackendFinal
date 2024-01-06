# models/publicacion.py
from utils.database import db  # Import the shared database instance
from .especie import Especie
from .raza import Raza
from .usuario import Usuario

class Publicacion(db.Model):
    __tablename__ = 'Publicacion'

    publicacionId = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    longitud = db.Column(db.Numeric(10, 6))
    latitud = db.Column(db.Numeric(10, 6))
    descripcion = db.Column(db.String(1000), nullable=False)
    rutaImg = db.Column(db.String(1000))
    especieId = db.Column(db.Integer, db.ForeignKey('Especie.id'), nullable=False)
    razaId = db.Column(db.Integer, db.ForeignKey('Raza.id'))
    usuarioId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)

    especie = db.relationship('Especie', backref=db.backref('publicaciones', lazy=True))
    raza = db.relationship('Raza', backref=db.backref('publicaciones', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('publicaciones', lazy=True))

    def __init__(self, tipo, fecha, longitud, latitud, descripcion, rutaImg, especieId, razaId, usuarioId):
        self.tipo = tipo
        self.fecha = fecha
        self.longitud = longitud
        self.latitud = latitud
        self.descripcion = descripcion
        self.rutaImg = rutaImg
        self.especieId = especieId
        self.razaId = razaId
        self.usuarioId = usuarioId

    # Additional methods and properties can be defined here
