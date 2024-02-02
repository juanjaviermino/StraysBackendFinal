from flask import Blueprint, request, jsonify
from sqlalchemy import func
from models.publicacion import Publicacion
from models.ciudad import Ciudad
from models.raza import Raza
from models.especie import Especie
from models.usuario import Usuario
from utils.database import db
import datetime
from services.storage_service import StorageService  # Asegúrate de importar tu StorageService

publicacion_blueprint = Blueprint('publicacion_blueprint', __name__)

storage_service = StorageService(bucket_name='straysimagesbucket')

@publicacion_blueprint.route('/publicaciones', methods=['POST'])
def create_publicacion():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    try:
        # Usa el servicio de almacenamiento para subir el archivo y obtener la URL
        file_url = storage_service.upload_file(file)

        # Recuperar otros datos del formulario
        data = request.form
        razaId = data.get('razaId')
        razaId = int(razaId) if razaId and razaId.strip() else None

        new_publicacion = Publicacion(
            tipo=data.get('tipo'),
            fecha=datetime.datetime.strptime(data.get('fecha'), '%Y-%m-%d').date(),
            longitud=data.get('longitud', type=float),
            latitud=data.get('latitud', type=float),
            descripcion=data.get('descripcion'),
            rutaImg=file_url,
            especieId=data.get('especieId', type=int),
            razaId=razaId,
            usuarioId=data.get('usuarioId', type=int)
        )

        db.session.add(new_publicacion)
        db.session.commit()
        return jsonify({'message': 'Publicacion created successfully', 'publicacionId': new_publicacion.publicacionId}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@publicacion_blueprint.route('/publicaciones/compare', methods=['POST'])
def compare_publicaciones():
    # Extract data from request body
    data = request.get_json()
    publicacion_id = data.get('publicacionId')
    additional_ids = data.get('publicacionesIds', [])

    # Fetch the single publication data
    single_publicacion = Publicacion.query.get(publicacion_id)
    if not single_publicacion:
        return jsonify({'error': 'Publicacion not found'}), 404

    # Define the query
    query = Publicacion.query.filter(Publicacion.especieId == single_publicacion.especieId, 
                                     Publicacion.tipo != single_publicacion.tipo,
                                     Publicacion.usuarioId != single_publicacion.usuarioId)

    # Filter based on additional IDs if provided
    if additional_ids:
        query = query.filter(Publicacion.publicacionId.in_(additional_ids))

    # Exclude the single publicacion ID
    query = query.filter(Publicacion.publicacionId != publicacion_id)

    # Fetch and prepare the image URLs
    images = [publicacion.rutaImg for publicacion in query.all()]

    results = {'base_image': single_publicacion.rutaImg, 'compare_images': images}

    return jsonify(results)


# Get publicacions by image routes
@publicacion_blueprint.route('/publicaciones/by-images', methods=['POST'])
def get_publicaciones_by_images():
    data = request.get_json()
    img_routes = data.get('imgRoutes', [])

    if not img_routes:
        return jsonify({'error': 'No image routes provided'}), 400

    # Query for publicaciones with related data
    publicaciones = Publicacion.query.filter(Publicacion.rutaImg.in_(img_routes))\
                                     .join(Especie)\
                                     .join(Raza)\
                                     .join(Usuario)\
                                     .join(Ciudad)\
                                     .all()

    publicaciones_data = [{
        'publicacionId': pub.publicacionId,
        'tipo': pub.tipo,
        'fecha': pub.fecha.isoformat(),
        'longitud': str(pub.longitud),
        'latitud': str(pub.latitud),
        'descripcion': pub.descripcion,
        'rutaImg': pub.rutaImg,
        'especie': pub.especie.especie,
        'raza': pub.raza.raza if pub.raza else None,
        'usuario': {
            'id': pub.usuario.id,
            'name': pub.usuario.name,
            'lastname': pub.usuario.lastname,
            'cellphone': pub.usuario.cellphone,
            'ciudad': pub.usuario.ciudad.nombre
        }
    } for pub in publicaciones]

    return jsonify(publicaciones_data)


@publicacion_blueprint.route('/publicaciones/filter', methods=['GET'])
def filter_publicaciones():
    # Extract query parameters
    especie_id = request.args.get('especieId', type=int)
    raza_id = request.args.get('razaId', type=int)
    usuario_id = request.args.get('usuarioId', type=int)
    ciudad_id = request.args.get('ciudadId', type=int)
    tipo = request.args.get('tipo')
    fecha_start = request.args.get('fechaStart')
    fecha_end = request.args.get('fechaEnd')
    publicacion_id = request.args.get('publicacionId', type=int)

    # Build a dynamic query
    query = Publicacion.query

    if especie_id:
        query = query.filter(Publicacion.especieId == especie_id)
    if raza_id:
        query = query.filter(Publicacion.razaId == raza_id)
    if usuario_id:
        query = query.filter(Publicacion.usuarioId == usuario_id)
    if ciudad_id:
        query = query.join(Usuario).filter(Usuario.ciudadId == ciudad_id)
    if publicacion_id:
        query = query.filter(Publicacion.publicacionId == publicacion_id)
    if tipo:
        query = query.filter(Publicacion.tipo == tipo)
    if fecha_start:
        query = query.filter(Publicacion.fecha >= datetime.datetime.strptime(fecha_start, '%Y-%m-%d').date())
    if fecha_end:
        query = query.filter(Publicacion.fecha <= datetime.datetime.strptime(fecha_end, '%Y-%m-%d').date())

    query = query.order_by(Publicacion.fecha.desc())
    # Fetch the results
    publicaciones = query.all()

    # Serialize the results
    publicaciones_data = [{
        'publicacionId': pub.publicacionId,
        'tipo': pub.tipo,
        'fecha': pub.fecha.isoformat(),
        'longitud': str(pub.longitud),
        'latitud': str(pub.latitud),
        'descripcion': pub.descripcion,
        'rutaImg': pub.rutaImg,
        'especie': pub.especie.especie,
        'raza': pub.raza.raza if pub.raza else None,
        'usuario': {
            'id': pub.usuario.id,
            'name': pub.usuario.name,
            'lastname': pub.usuario.lastname,
            'cellphone': pub.usuario.cellphone,
            'ciudad': pub.usuario.ciudad.nombre
        }
    } for pub in publicaciones]

    return jsonify(publicaciones_data)


@publicacion_blueprint.route('/publicaciones/<int:publicacion_id>', methods=['GET'])
def get_publicacion_by_id(publicacion_id):
    publicacion = Publicacion.query.filter_by(publicacionId=publicacion_id)\
                                   .join(Especie)\
                                   .join(Raza, isouter=True)\
                                   .join(Usuario)\
                                   .join(Ciudad, isouter=True)\
                                   .first()

    if not publicacion:
        return jsonify({'error': 'Publicacion not found'}), 404

    publicacion_data = {
        'publicacionId': publicacion.publicacionId,
        'tipo': publicacion.tipo,
        'fecha': publicacion.fecha.isoformat(),
        'longitud': str(publicacion.longitud),
        'latitud': str(publicacion.latitud),
        'descripcion': publicacion.descripcion,
        'rutaImg': publicacion.rutaImg,
        'especie': publicacion.especie.especie,
        'raza': publicacion.raza.raza if publicacion.raza else None,
        'usuario': {
            'id': publicacion.usuario.id,
            'name': publicacion.usuario.name,
            'lastname': publicacion.usuario.lastname,
            'cellphone': publicacion.usuario.cellphone,
            'ciudad': publicacion.usuario.ciudad.nombre if publicacion.usuario.ciudad else None
        }
    }

    return jsonify(publicacion_data)

@publicacion_blueprint.route('/publicaciones/count_by_raza', methods=['GET'])
def count_publicaciones_by_raza():
    especie_id = request.args.get('especieId', type=int)
    raza_id = request.args.get('razaId', type=int)
    usuario_id = request.args.get('usuarioId', type=int)
    ciudad_id = request.args.get('ciudadId', type=int)
    tipo = request.args.get('tipo')
    fecha_start = request.args.get('fechaStart')
    fecha_end = request.args.get('fechaEnd')
    publicacion_id = request.args.get('publicacionId', type=int)

    query = db.session.query(Raza.raza, func.count(Publicacion.publicacionId).label('count')).outerjoin(Publicacion, Raza.id == Publicacion.razaId)

    if especie_id:
        query = query.filter(Publicacion.especieId == especie_id)
    if raza_id:
        query = query.filter(Publicacion.razaId == raza_id)
    if usuario_id:
        query = query.filter(Publicacion.usuarioId == usuario_id)
    if ciudad_id:
        query = query.join(Usuario, Publicacion.usuarioId == Usuario.id).filter(Usuario.ciudadId == ciudad_id)
    if publicacion_id:
        query = query.filter(Publicacion.publicacionId == publicacion_id)
    if tipo:
        query = query.filter(Publicacion.tipo == tipo)
    if fecha_start:
        query = query.filter(Publicacion.fecha >= datetime.datetime.strptime(fecha_start, '%Y-%m-%d').date())
    if fecha_end:
        query = query.filter(Publicacion.fecha <= datetime.datetime.strptime(fecha_end, '%Y-%m-%d').date())

    query = query.group_by(Raza.raza).order_by(func.count(Publicacion.publicacionId).desc())

    query = query.limit(15)

    results = query.all()

    raza_count_data = [{'raza': raza, 'count': count} for raza, count in results]

    return jsonify(raza_count_data)