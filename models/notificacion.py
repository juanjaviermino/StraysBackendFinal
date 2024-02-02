# models/notificacion.py
from utils.database import db  # Import the shared instance

class Notificacion(db.Model):
    __tablename__ = 'Notificacion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    publicacionId = db.Column(db.Integer, db.ForeignKey('Publicacion.publicacionId'), nullable=False)
    mensaje = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    leida = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    usuario = db.relationship('Usuario', backref=db.backref('notificaciones', lazy=True))
    publicacion = db.relationship('Publicacion', backref=db.backref('notificaciones', lazy=True))

    def __init__(self, userId, publicacionId, mensaje):
        self.userId = userId
        self.publicacionId = publicacionId
        self.mensaje = mensaje

    # Additional methods and properties can be defined here
