from flask import Blueprint, request, jsonify
from models.raza import Raza
from models.especie import Especie
from utils.database import db

raza_blueprint = Blueprint('raza_blueprint', __name__)

# CREATE 
@raza_blueprint.route('/raza', methods=['POST'])
def create_raza():
    data = request.get_json()
    new_raza = Raza(raza=data['raza'], especieId=data['especieId'])
    db.session.add(new_raza)
    db.session.commit()
    return jsonify({
        'message': 'Raza created successfully',
        'raza': {
            'id': new_raza.id,
            'raza': new_raza.raza,
            'especieId': new_raza.especieId
        }
    }), 201

# GET ALL
@raza_blueprint.route('/raza', methods=['GET'])
def get_all_razas():
    razas = Raza.query.join(Especie, Raza.especieId == Especie.id).all()
    raza_list = [{
        'id': raza.id,
        'raza': raza.raza,
        'especie': raza.especie.especie,
        'especieId': raza.especieId,
    } for raza in razas]
    return jsonify(raza_list), 200

# GET Razas by Especie ID
@raza_blueprint.route('/raza/especie/<int:especie_id>', methods=['GET'])
def get_razas_by_especie(especie_id):
    razas = Raza.query.filter_by(especieId=especie_id).all()
    raza_list = [{
        'id': raza.id,
        'raza': raza.raza,
        'especie': raza.especie.especie,
        'especieId': raza.especieId,
    } for raza in razas]
    return jsonify(raza_list), 200

# GET ONE
@raza_blueprint.route('/raza/<int:id>', methods=['GET'])
def get_raza(id):
    raza = Raza.query.join(Especie, Raza.especieId == Especie.id).filter(Raza.id == id).first_or_404()
    return jsonify({
        'id': raza.id,
        'raza': raza.raza,
        'especie': raza.especie.especie,
        'especieId': raza.especieId,
    }), 200

# EDIT
@raza_blueprint.route('/raza/<int:id>', methods=['PUT'])
def update_raza(id):
    data = request.get_json()
    raza = Raza.query.get_or_404(id)
    raza.raza = data['raza']
    raza.especieId = data['especieId']
    db.session.commit()
    return jsonify({
        'message': 'Raza updated successfully',
        'raza': {
            'id': raza.id,
            'raza': raza.raza,
            'especieId': raza.especieId
        }
    }), 200

# DELETE
@raza_blueprint.route('/raza/<int:id>', methods=['DELETE'])
def delete_raza(id):
    raza = Raza.query.get_or_404(id)
    db.session.delete(raza)
    db.session.commit()
    return jsonify({'message': 'Raza deleted successfully'}), 200
