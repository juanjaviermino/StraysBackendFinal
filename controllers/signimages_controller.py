from flask import Blueprint, request, jsonify
from google.cloud import storage
from google.oauth2 import service_account
import os
from urllib.parse import urlparse

# Initialize Google Cloud Storage client
credentials = service_account.Credentials.from_service_account_file('silicon-brace-410116-7c097b027311.json')
storage_client = storage.Client(credentials=credentials)
bucket_name = 'straysimagesbucket'

sign_images_blueprint = Blueprint('sign_images_blueprint', __name__)

@sign_images_blueprint.route('/signedUrl', methods=['GET'])
def get_signed_url():
    full_url = request.args.get('filePath')
    parsed_url = urlparse(full_url)
    file_path = os.path.basename(parsed_url.path)
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)

    # Generate signed URL
    signed_url = blob.generate_signed_url(version='v4', expiration=3600, method='GET')

    return jsonify({'signedUrl': signed_url})
