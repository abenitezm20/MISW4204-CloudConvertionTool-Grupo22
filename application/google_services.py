import os

from config import CREDENTIALS_FOLDER
from google.cloud import storage
from helper import filepath

class GoogleService ():
    client_bucket = None

    @staticmethod
    def get_storage_client():
        if GoogleService.client_bucket:
            return GoogleService.client_bucket
        
        bucket_name = os.getenv('GOOGLE_BUCKET')
        google_config_file = os.getenv('GOOGLE_ACCESS_FILE')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(CREDENTIALS_FOLDER, google_config_file)

        storage_client = storage.Client()
        GoogleService.client_bucket = storage_client.bucket(bucket_name)

        return GoogleService.client_bucket
    
    @staticmethod
    def save_file(filepath, filename):
        blob = GoogleService.get_storage_client().blob(filename)
        blob.upload_from_filename(filepath)

        return True
    
    @staticmethod
    def get_file(filenamepath, filename):
        blob = GoogleService.get_storage_client().blob(filename)
        blob.download_to_filename(filenamepath)

        return True
