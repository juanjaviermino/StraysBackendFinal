from flask import Blueprint, request, jsonify
from utils.database import db
from models.usuario import Usuario
from models.ciudad import Ciudad
from models.publicacion import Publicacion
from models.notificacion import Notificacion
from services.email_service import send_email
from services.GoogleMapsgeolocation_service import GoogleMapsGeoLocationService

notificacion_blueprint = Blueprint('notificacion_blueprint', __name__)

@notificacion_blueprint.route('/notificacion', methods=['POST'])
def create_notificacion():
    data = request.get_json()
    latitud = data['latitud']
    longitud = data['longitud']
    publicacionId = data['publicacionId']

    # Obtener detalles de la publicación
    publicacion = Publicacion.query.get(publicacionId)
    if not publicacion:
        return jsonify({'message': 'Publicación no encontrada.'}), 404

    # Utilizar GeoLocationService para obtener el nombre de la ciudad
    api_key = "AIzaSyBfLn8UnPuDdKsXa_uHsvF83Q18no7AmR8"
    geo_service = GoogleMapsGeoLocationService(api_key=api_key)
    ciudad_nombre = geo_service.get_city_name_by_coordinates(latitud, longitud)

    if not ciudad_nombre:
        return jsonify({'message': 'No se pudo determinar la ciudad para las coordenadas dadas.'}), 400

    # Buscar la ciudad por nombre
    ciudad = Ciudad.query.filter_by(nombre=ciudad_nombre).first()
    if not ciudad:
        # Si la ciudad no existe, la operación termina aquí
        return jsonify({'message': f'Ciudad {ciudad_nombre} creada. No existen usuarios para notificar.'}), 201

    # Obtener todos los usuarios de esa ciudad, excluyendo al usuario que creó la publicación
    usuarios = Usuario.query.filter(Usuario.ciudadId == ciudad.id, Usuario.id != publicacion.usuarioId).all()

    # Crear notificación para cada usuario
    for usuario in usuarios:
        # Convertir el tipo de la publicación de inglés a español
        tipo_espanol = "perdido" if publicacion.tipo == "lost" else "encontrado"
        mensaje = f"Nuevo {publicacion.especie.especie} {tipo_espanol} cerca de ti"
        nueva_notificacion = Notificacion(userId=usuario.id, publicacionId=publicacion.publicacionId, mensaje=mensaje)
        db.session.add(nueva_notificacion)

    db.session.commit()

    for usuario in usuarios:
        send_email(subject='Nueva Notificación de Mascota',
                   to_email=[usuario.email],
                   body=f'Hola {usuario.name}, tienes una nueva notificación: {mensaje}')

    return jsonify({'message': 'Notificaciones creadas exitosamente para usuarios en ' + ciudad_nombre}), 201


@notificacion_blueprint.route('/notificaciones/usuario/<int:user_id>', methods=['GET'])
def get_notificaciones_by_user(user_id):
    # Buscar todas las notificaciones para el usuario con user_id
    notificaciones = Notificacion.query.filter_by(userId=user_id).join(Publicacion, Notificacion.publicacionId == Publicacion.publicacionId).all()

    if not notificaciones:
        return jsonify({'message': 'No se encontraron notificaciones para el usuario.'}), 404

    # Preparar los datos de las notificaciones para la respuesta
    notificaciones_data = []
    for notificacion in notificaciones:
        # Formatear fecha y hora
        fecha_formato = notificacion.fecha.strftime('%d/%m/%Y')
        hora_formato = notificacion.fecha.strftime('%H:%M')

        notificacion_data = {
            'id':notificacion.id,
            'mensaje': notificacion.mensaje,
            'fecha': fecha_formato,
            'hora': hora_formato,
            'leida': notificacion.leida,
            'publicacionId': notificacion.publicacionId,
            'latitud': notificacion.publicacion.latitud,
            'longitud': notificacion.publicacion.longitud
        }
        notificaciones_data.append(notificacion_data)

    return jsonify(notificaciones_data), 200


@notificacion_blueprint.route('/notificacion/<int:notificacion_id>', methods=['PATCH'])
def marcar_notificacion_como_leida(notificacion_id):
    # Buscar la notificación por ID
    notificacion = Notificacion.query.get(notificacion_id)
    
    # Verificar si la notificación existe
    if not notificacion:
        return jsonify({'message': 'Notificación no encontrada.'}), 404
    
    # Actualizar el estado leida de la notificación a True
    notificacion.leida = True
    db.session.commit()
    
    return jsonify({
        'message': 'Notificación marcada como leída.',
        'notificacion': {
            'id': notificacion.id,
            'mensaje': notificacion.mensaje,
            'fecha': notificacion.fecha.strftime('%d/%m/%Y %H:%M'),
            'leida': notificacion.leida,
            'publicacionId': notificacion.publicacionId
        }
    }), 200


