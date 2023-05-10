from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import Tarea, Usuario
from vistas import db, Tareas, GestionTareas, Health, GestionArchivos, Registrar, Autenticar, Procesar
from helper import encrypt
from application import create_app
from pubsub_subscriber import SubscriberHandler

app, celery = create_app()
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)

db.create_all()

SubscriberHandler.block_if_is_worker()

cors = CORS(app)

api = Api(app)
api.add_resource(Registrar, '/api/auth/signup')
api.add_resource(Autenticar, '/api/auth/login')
api.add_resource(Tareas, '/api/tasks')
api.add_resource(GestionTareas, '/api/tasks/<int:id_task>')
api.add_resource(GestionArchivos, '/api/files/<filename>')
api.add_resource(Health, '/health')
api.add_resource(Procesar, '/procesar')