# STRAYS

STRAYS es una aplicación web diseñada para facilitar la reunión de mascotas perdidas con sus familias. A través de una plataforma intuitiva, los usuarios pueden publicar anuncios de mascotas perdidas o encontradas, incluyendo detalles importantes como imágenes, tipo de animal, raza, y ubicación. Utilizando tecnologías modernas de frontend y backend, STRAYS ofrece una solución eficaz para abordar el problema de mascotas perdidas.

## Características

- **Publicación de Anuncios:** Los usuarios pueden crear anuncios para mascotas perdidas o encontradas, proporcionando detalles esenciales y fotos.
- **Reconocimiento de Imágenes:** Integración con un servicio de reconocimiento de imágenes para sugerir posibles coincidencias basadas en las fotos subidas.
- **Filtrado Avanzado:** Búsqueda y filtrado de anuncios por tipo de mascota, raza, y ubicación.
- **Implementación de Geolocalización:** Utilizamos la API de Google Maps para permitir a los usuarios seleccionar la ubicación exacta de la mascota mediante un mapa interactivo, mejorando la precisión de las publicaciones y las búsquedas.

## Tecnologías Utilizadas

- **Frontend:** React.js
- **Backend:** Flask (Python)
- **Base de Datos:** PostgreSQL
- **Servicios Externos:** Google Maps API para geolocalización, servicio de reconocimiento de imágenes.

## Estructura del Proyecto

El proyecto se divide en dos partes principales: frontend y backend.

- `/frontend`: Contiene todos los archivos relacionados con la interfaz de usuario de React.
- `/backend`: Incluye la API de Flask, modelos de datos, y controladores.

En este repositorio solamente se encuentra el backend.

### Modelos

Los modelos representan la estructura de datos de nuestras entidades principales: Usuarios, Publicaciones, Notificaciones, Ciudades, etc.

### Controladores

Los controladores manejan la lógica de negocio y las interacciones entre el frontend, la base de datos, y servicios externos.

## Instalación y Configuración

Para configurar y ejecutar STRAYS localmente, sigue estos pasos:

1. Clona el repositorio.
2. Configura tu entorno virtual de Python e instala las dependencias del backend con `pip install -r requirements.txt`.
3. Ejecuta el backend con `flask run`.
