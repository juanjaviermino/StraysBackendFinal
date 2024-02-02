# services/storage_service.py

from google.cloud import storage
from google.oauth2 import service_account
from werkzeug.utils import secure_filename
import os
import uuid

class StorageService:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        credentials_path = 'silicon-brace-410116-7c097b027311.json'
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = storage.Client(credentials=credentials)
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, file):
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(f"{uuid.uuid4()}{ext}")
            blob = self.bucket.blob(filename)
            blob.upload_from_string(file.read(), content_type=file.content_type)
            return blob.public_url
        else:
            raise ValueError("No file provided or file without a filename.")
