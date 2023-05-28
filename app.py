from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from vistas import db, Tareas, GestionTareas, Health, GestionArchivos, Registrar, Autenticar, Procesar, RecibirTarea
from application import create_app
from pubsub_subscriber import SubscriberHandler
import os

app, celery = create_app()
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)

db.create_all()

#is_worker = os.getenv('IS_WORKER')
#if is_worker is not None:
#    SubscriberHandler.start_subscriber(app)

cors = CORS(app)

api = Api(app)
api.add_resource(Registrar, '/api/auth/signup')
api.add_resource(Autenticar, '/api/auth/login')
api.add_resource(Tareas, '/api/tasks')
api.add_resource(GestionTareas, '/api/tasks/<int:id_task>')
api.add_resource(GestionArchivos, '/api/files/<filename>')
api.add_resource(Procesar, '/procesar')
api.add_resource(Health, '/health')
api.add_resource(RecibirTarea, '/recibir')