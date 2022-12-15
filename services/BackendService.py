import os
import random
import time
from firebase_admin import credentials, initialize_app, storage

import requests
import json

class BackendService:
    def __init__(self, database) -> None:
        self.database_url = os.getenv('FIREBASE_APP_URL')
        self.credential = credentials.Certificate("key.json")
        self.bucket_name = os.getenv('FIREBASE_BUCKET_NAME')
        initialize_app(self.credential)
    
    def upload_image(self, name, image):
        bucket = storage.bucket(self.bucket_name)
        blob = bucket.blob(name)
        blob.upload_from_string(image, content_type='image/png')
        return blob.public_url