#!C:\Users\jmino\AppData\Local\Programs\Python\Python3.9\python.exe
# app.py
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Database configuration
# Replace with your actual Google Cloud SQL credentials
username = 'postgres'
password = 'strays1801'
host = '34.72.22.251'
dbname = 'postgres'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}/{dbname}'
app.config['UPLOAD_FOLDER'] = r'D:\STRAYS Final\StraysMicroservice\postImages'
CORS(app)  # Middleware for interacting with your React serve

from utils.database import db
db.init_app(app)

# Blueprint registration: 

# Import the provincia_blueprint
from controllers.provincia_controller import provincia_blueprint
app.register_blueprint(provincia_blueprint)

# Import the ciudad blueprint
from controllers.ciudad_controller import ciudad_blueprint
app.register_blueprint(ciudad_blueprint)

# Import the especie blueprint
from controllers.especie_controller import especie_blueprint
app.register_blueprint(especie_blueprint)

# Import the raza blueprint
from controllers.raza_controller import raza_blueprint
app.register_blueprint(raza_blueprint)

# Import the usuario blueprint
from controllers.usuario_controller import user_blueprint
app.register_blueprint(user_blueprint)

# Import the publicacion blueprint
from controllers.publicacion_controller import publicacion_blueprint
app.register_blueprint(publicacion_blueprint)

# Import the color_publicacion blueprint
from controllers.color_publicacion_controller import color_publicacion_blueprint
app.register_blueprint(color_publicacion_blueprint)

# Import the sign_images_blueprint blueprint
from controllers.signimages_controller import sign_images_blueprint
app.register_blueprint(sign_images_blueprint)

sign_images_blueprint

if __name__ == "__main__":
    app.run(debug=True)