from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import Tarea, Usuario
from vistas import db, Tareas, GestionTareas, Health, GestionArchivos, Registrar, Autenticar, Procesar
from helper import encrypt
from application import create_app
from pubsub_subscriber import SubscriberHandler
# from application.google_services import GoogleService
# from tasks import compress_task

import os
import json

app, celery = create_app()
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)

db.create_all()

is_worker = os.getenv('IS_WORKER')
if is_worker is not None:
    SubscriberHandler.start_subscriber(app)
    
    # def callback(message):
    #     print(f'message is: {message}')
    #     data = message.data.decode()
    #     print(f'data is: {data}')
    #     data = json.loads(data)
    #     # {"id": 11}
    #     task_id = data.get('id')
    #     message.ack()
    #     with app.app_context():
    #         compress_task(task_id)

    # streaming_future = GoogleService.pubsub_subscribe(callback)
    # print('listening...')

    # with GoogleService.get_pubsub_subscriber_client():
    #     try:
    #         streaming_future.result()
    #     except ValueError:
    #         streaming_future.cancel()
    #         streaming_future.result()


cors = CORS(app)

api = Api(app)
api.add_resource(Registrar, '/api/auth/signup')
api.add_resource(Autenticar, '/api/auth/login')
api.add_resource(Tareas, '/api/tasks')
api.add_resource(GestionTareas, '/api/tasks/<int:id_task>')
api.add_resource(GestionArchivos, '/api/files/<filename>')
api.add_resource(Health, '/health')
api.add_resource(Procesar, '/procesar')