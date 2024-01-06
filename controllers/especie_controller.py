from flask import Blueprint, request, jsonify
from models.especie import Especie
from utils.database import db

especie_blueprint = Blueprint('especie_blueprint', __name__)

# CREATE 
@especie_blueprint.route('/especie', methods=['POST'])
def create_especie():
    data = request.get_json()
    new_especie = Especie(especie=data['especie'])
    db.session.add(new_especie)
    db.session.commit()
    return jsonify({'message': 'Especie created successfully', 'especie': {'id': new_especie.id, 'especie': new_especie.especie}}), 201

# GET ALL
@especie_blueprint.route('/especie', methods=['GET'])
def get_all_especies():
    especies = Especie.query.all()
    return jsonify([{'id': especie.id, 'especie': especie.especie} for especie in especies]), 200

# GET ONE
@especie_blueprint.route('/especie/<int:id>', methods=['GET'])
def get_especie(id):
    especie = Especie.query.get_or_404(id)
    return jsonify({'id': especie.id, 'especie': especie.especie}), 200

# EDIT
@especie_blueprint.route('/especie/<int:id>', methods=['PUT'])
def update_especie(id):
    data = request.get_json()
    especie = Especie.query.get_or_404(id)
    especie.especie = data['especie']
    db.session.commit()
    return jsonify({'message': 'Especie updated successfully', 'especie': {'id': especie.id, 'especie': especie.especie}}), 200

# DELETE
@especie_blueprint.route('/especie/<int:id>', methods=['DELETE'])
def delete_especie(id):
    especie = Especie.query.get_or_404(id)
    db.session.delete(especie)
    db.session.commit()
    return jsonify({'message': 'Especie deleted successfully'}), 200
