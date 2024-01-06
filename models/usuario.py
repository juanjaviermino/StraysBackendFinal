# models/usuario.py
from utils.database import db  # Import the shared instance
from .ciudad import Ciudad

class Usuario(db.Model):
    __tablename__ = 'Usuario'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cellphone = db.Column(db.String(30))
    role = db.Column(db.String(20), nullable=False, default='USER')
    ciudadId = db.Column(db.Integer, db.ForeignKey('Ciudad.id'))

    ciudad = db.relationship('Ciudad', backref=db.backref('usuarios', lazy=True))

    def __init__(self, name, lastname, email, password, cellphone, role, ciudadId):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.cellphone = cellphone
        self.role = role
        self.ciudadId = ciudadId

    # Additional methods and properties can be defined here
