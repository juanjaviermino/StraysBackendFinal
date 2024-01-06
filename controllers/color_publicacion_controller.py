from flask import Blueprint, request, jsonify
from models.color_publicacion import ColorPublicacion
from models.publicacion import Publicacion
from utils.database import db

color_publicacion_blueprint = Blueprint('color_publicacion_blueprint', __name__)

# CREATE 
@color_publicacion_blueprint.route('/color_publicacion', methods=['POST'])
def create_color_publicacion():
    data = request.get_json()
    new_color_publicacion = ColorPublicacion(color=data['color'], publicacionId=data['publicacionId'])
    db.session.add(new_color_publicacion)
    db.session.commit()
    return jsonify({'message': 'ColorPublicacion created successfully', 'color_publicacion': {'id': new_color_publicacion.id, 'color': new_color_publicacion.color, 'publicacionId': new_color_publicacion.publicacionId}}), 201

# GET ALL
@color_publicacion_blueprint.route('/color_publicacion', methods=['GET'])
def get_all_color_publicaciones():
    color_publicaciones = ColorPublicacion.query.all()
    return jsonify([{'id': cp.id, 'color': cp.color, 'publicacionId': cp.publicacionId} for cp in color_publicaciones]), 200

# GET ONE
@color_publicacion_blueprint.route('/color_publicacion/<int:id>', methods=['GET'])
def get_color_publicacion(id):
    color_publicacion = ColorPublicacion.query.get_or_404(id)
    return jsonify({'id': color_publicacion.id, 'color': color_publicacion.color, 'publicacionId': color_publicacion.publicacionId}), 200

# EDIT
@color_publicacion_blueprint.route('/color_publicacion/<int:id>', methods=['PUT'])
def update_color_publicacion(id):
    data = request.get_json()
    color_publicacion = ColorPublicacion.query.get_or_404(id)
    color_publicacion.color = data['color']
    color_publicacion.publicacionId = data['publicacionId']
    db.session.commit()
    return jsonify({'message': 'ColorPublicacion updated successfully', 'color_publicacion': {'id': color_publicacion.id, 'color': color_publicacion.color, 'publicacionId': color_publicacion.publicacionId}}), 200

# DELETE
@color_publicacion_blueprint.route('/color_publicacion/<int:id>', methods=['DELETE'])
def delete_color_publicacion(id):
    color_publicacion = ColorPublicacion.query.get_or_404(id)
    db.session.delete(color_publicacion)
    db.session.commit()
    return jsonify({'message': 'ColorPublicacion deleted successfully'}), 200

# GET COLORS BY PUBLICACION
@color_publicacion_blueprint.route('/color_publicacion/comparar/<int:publicacion_id>', methods=['GET'])
def get_similar_publications(publicacion_id):
    # Query for colors related to the provided publicacionId
    related_colors = ColorPublicacion.query.filter_by(publicacionId=publicacion_id).all()

    if not related_colors:
        return jsonify([]), 200

    similar_publications = set()
    # Iterate over each color and find publications with similar colors
    for color in related_colors:
        similar_colors = ColorPublicacion.query.filter(ColorPublicacion.color == color.color, 
                                                       ColorPublicacion.publicacionId != publicacion_id).all()
        for similar_color in similar_colors:
            similar_publications.add(similar_color.publicacionId)

    # Convert set to list and remove duplicates
    similar_publications_list = list(similar_publications)
    
    return jsonify(similar_publications_list), 200