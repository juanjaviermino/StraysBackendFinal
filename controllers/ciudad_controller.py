from flask import Blueprint, request, jsonify
from models.ciudad import Ciudad
from models.provincia import Provincia
from utils.database import db 

ciudad_blueprint = Blueprint('ciudad_blueprint', __name__)

# CREATE 
@ciudad_blueprint.route('/ciudad', methods=['POST'])
def create_ciudad():
    data = request.get_json()
    new_ciudad = Ciudad(nombre=data['nombre'], provinciaId=data['provinciaId'])
    db.session.add(new_ciudad)
    db.session.commit()
    return jsonify({
        'message': 'Ciudad created successfully',
        'ciudad': {
            'id': new_ciudad.id,
            'nombre': new_ciudad.nombre,
            'provinciaId': new_ciudad.provinciaId
        }
    }), 201

# GET ALL
@ciudad_blueprint.route('/ciudad', methods=['GET'])
def get_all_ciudades():
    ciudades = Ciudad.query.join(Provincia, Ciudad.provinciaId == Provincia.id).all()
    ciudad_list = [{
        'id': ciudad.id,
        'nombre': ciudad.nombre,
        'provincia': ciudad.provincia.nombre,
        'provinciaId': ciudad.provinciaId
    } for ciudad in ciudades]
    return jsonify(ciudad_list), 200

# GET ONE
@ciudad_blueprint.route('/ciudad/<int:id>', methods=['GET'])
def get_ciudad(id):
    ciudad = Ciudad.query.join(Provincia, Ciudad.provinciaId == Provincia.id).filter(Ciudad.id == id).first_or_404()
    return jsonify({
        'id': ciudad.id,
        'nombre': ciudad.nombre,
        'provincia': ciudad.provincia.nombre,
        'provinciaId': ciudad.provinciaId
    }), 200

# EDIT
@ciudad_blueprint.route('/ciudad/<int:id>', methods=['PUT'])
def update_ciudad(id):
    data = request.get_json()
    ciudad = Ciudad.query.get_or_404(id)
    ciudad.nombre = data['nombre']
    ciudad.provinciaId = data['provinciaId']
    db.session.commit()
    return jsonify({
        'message': 'Ciudad updated successfully',
        'ciudad': {
            'id': ciudad.id,
            'nombre': ciudad.nombre,
            'provinciaId': ciudad.provinciaId
        }
    }), 200

# DELETE
@ciudad_blueprint.route('/ciudad/<int:id>', methods=['DELETE'])
def delete_ciudad(id):
    ciudad = Ciudad.query.get_or_404(id)
    db.session.delete(ciudad)
    db.session.commit()
    return jsonify({'message': 'Ciudad deleted successfully'}), 200
