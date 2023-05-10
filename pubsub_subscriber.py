from application.google_services import GoogleService
from tasks import compress_task
import os
import json

class SubscriberHandler():

    # app_context = None

    # @staticmethod
    # def read_message(message):
    #     print(f'message is: {message}')
    #     data = message.data.decode()
    #     print(f'data is: {data}')
    #     data = json.loads(data)
    #     # {"id": 11}
    #     task_id = data.get('id')
    #     # with SubscriberHandler.app_context:
    #     compress_task(task_id)
    #     message.ack()

    @staticmethod
    def start_subscriber(app):

        def callback(message):
            print(f'message is: {message}')
            data = message.data.decode()
            print(f'data is: {data}')
            data = json.loads(data)
            # {"id": 11}
            task_id = data.get('id')
            message.ack()
            with app.app_context():
                compress_task(task_id)

        streaming_future = GoogleService.pubsub_subscribe(callback)
        print('listening...')

        with GoogleService.get_pubsub_subscriber_client():
            try:
                streaming_future.result()
            except ValueError:
                streaming_future.cancel()
                streaming_future.result()
