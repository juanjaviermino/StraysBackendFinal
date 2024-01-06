from flask import Blueprint, request, jsonify
from models.provincia import Provincia
from utils.database import db 

provincia_blueprint = Blueprint('provincia_blueprint', __name__)

# CREATE 
@provincia_blueprint.route('/provincia', methods=['POST'])
def create_provincia():
    data = request.get_json()
    new_provincia = Provincia(nombre=data['nombre'])
    db.session.add(new_provincia)
    db.session.commit()
    return jsonify({'message': 'Provincia created successfully', 'provincia': {'id': new_provincia.id, 'nombre': new_provincia.nombre}}), 201

# GET ALL
@provincia_blueprint.route('/provincia', methods=['GET'])
def get_all_provincias():
    provincias = Provincia.query.all()
    return jsonify([{'id': prov.id, 'nombre': prov.nombre} for prov in provincias]), 200

# GET ONE
@provincia_blueprint.route('/provincia/<int:id>', methods=['GET'])
def get_provincia(id):
    provincia = Provincia.query.get_or_404(id)
    return jsonify({'id': provincia.id, 'nombre': provincia.nombre}), 200


# EDIT
@provincia_blueprint.route('/provincia/<int:id>', methods=['PUT'])
def update_provincia(id):
    data = request.get_json()
    provincia = Provincia.query.get_or_404(id)
    provincia.nombre = data['nombre']
    db.session.commit()
    return jsonify({'message': 'Provincia updated successfully', 'provincia': {'id': provincia.id, 'nombre': provincia.nombre}}), 200


# DELETE
@provincia_blueprint.route('/provincia/<int:id>', methods=['DELETE'])
def delete_provincia(id):
    provincia = Provincia.query.get_or_404(id)
    db.session.delete(provincia)
    db.session.commit()
    return jsonify({'message': 'Provincia deleted successfully'}), 200


