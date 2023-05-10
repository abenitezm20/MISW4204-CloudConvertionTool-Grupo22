import os
from google.cloud import storage, pubsub_v1
# from config import CREDENTIALS_FOLDER

class GoogleService ():
    client_bucket = None
    publisher = None
    subscriber = None
    topic_path = 'projects/cloud-convertion-tool-384419/topics/compress-task'
    subscriber_path = 'projects/cloud-convertion-tool-384419/subscriptions/compress-task-worker'


    @staticmethod
    def get_storage_client():
        if GoogleService.client_bucket:
            return GoogleService.client_bucket
        
        bucket_name = os.getenv('GOOGLE_BUCKET')

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
    

    # pubsub publisher client-------------------

    @staticmethod
    def get_pubsub_publisher_client():
        if GoogleService.publisher:
            return GoogleService.publisher

        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(CREDENTIALS_FOLDER, 'cloud-convertion-tool-storage.json')
        
        publisher = pubsub_v1.PublisherClient()
        GoogleService.publisher = publisher

        return GoogleService.publisher
    
    @staticmethod
    def pubsub_publish(message):
        encoded_message = message.encode('utf-8')
        return GoogleService.get_pubsub_publisher_client().publish(GoogleService.topic_path, encoded_message)


    # pubsub subscriber client-------------------

    @staticmethod
    def get_pubsub_subscriber_client():
        if GoogleService.subscriber:
            return GoogleService.subscriber
        
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(CREDENTIALS_FOLDER, 'cloud-convertion-tool-storage.json')
        
        subscriber = pubsub_v1.SubscriberClient()
        GoogleService.subscriber = subscriber

        return GoogleService.subscriber
    
    @staticmethod
    def pubsub_subscribe(callback):
        return GoogleService.get_pubsub_subscriber_client().subscribe(GoogleService.subscriber_path, callback=callback)
