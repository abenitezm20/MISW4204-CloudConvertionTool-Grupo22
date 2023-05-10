from application.google_services import GoogleService
from tasks import compress_task
import os
import json

class SubscriberHandler():

    @staticmethod
    def read_message(message):
        data = message.data.decode()
        data = json.loads(data)
        # {"id": 11}
        task_id = data.get('id')
        compress_task(task_id)
        message.ack()

    @staticmethod
    def block_if_is_worker():
        is_worker = os.getenv('IS_WORKER')
        if is_worker is None:
            return

        SubscriberHandler.start_subscriber()

    @staticmethod
    def start_subscriber():
        streaming_future = GoogleService.pubsub_subscribe(SubscriberHandler.read_message)

        with GoogleService.get_pubsub_subscriber_client():
            try:
                streaming_future.result()
            except ValueError:
                streaming_future.cancel()
                streaming_future.result()
