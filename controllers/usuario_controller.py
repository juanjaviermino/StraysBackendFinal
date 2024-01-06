# controllers/user_controller.py
from flask import Blueprint, request, jsonify
from utils.database import db  # Import the shared instance
from models.usuario import Usuario
from models.ciudad import Ciudad
from sqlalchemy.exc import IntegrityError

user_blueprint = Blueprint('user_blueprint', __name__)

# POST a new user
@user_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        new_user = Usuario(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError:
        return jsonify({'message': 'Email already exists'}), 409
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# GET all users
@user_blueprint.route('/users', methods=['GET'])
def get_users():
    try:
        users = Usuario.query.with_entities(Usuario.id, Usuario.name, Usuario.lastname, Usuario.email, Usuario.cellphone, Usuario.role, Ciudad.nombre, Usuario.ciudadId).join(Ciudad, Usuario.ciudadId == Ciudad.id).all()
        return jsonify([{'id': u.id, 'name': u.name, 'lastname': u.lastname, 'email': u.email, 'cellphone': u.cellphone, 'role': u.role, 'ciudad': u.nombre, 'ciudadId': u.ciudadId} for u in users])
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# GET ONE
@user_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = Usuario.query.join(Ciudad, Usuario.ciudadId == Ciudad.id).filter(Usuario.id == id).first_or_404()
    return jsonify({
        'id': user.id,
        'name': user.name,
        'lastname': user.lastname,
        'email': user.email,
        'password': user.password,  # Be cautious about returning passwords
        'cellphone': user.cellphone,
        'role': user.role,
        'ciudadId': user.ciudadId,
        'ciudad': user.ciudad.nombre,
    }), 200

# DELETE a user by id
@user_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = Usuario.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# UPDATE a user by id
@user_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    try:
        user = Usuario.query.get(id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# POST for user authentication
@user_blueprint.route('/users/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    user = Usuario.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.password == password:
        user_data = {
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'cellphone': user.cellphone,
            'role': user.role
            #'password', and 'ciudad'
        }
        return jsonify({'authenticated': True, 'user': user_data}), 200
    else:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401


# PATCH a user by id
@user_blueprint.route('/users/<int:id>', methods=['PATCH'])
def patch_user(id):
    data = request.json
    user = Usuario.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        # Only update fields that are actually provided in the request
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
