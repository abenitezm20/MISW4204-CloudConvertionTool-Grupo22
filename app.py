import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from modelos import db
from vistas import Tareas, GestionTareas


DATABASE_URI = os.environ.get(
    'DATABASE_URI') or 'postgresql://admin:admin@localhost:5432/tool'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(Tareas, '/api/tasks')
api.add_resource(GestionTareas, '/api/tasks/<int:id_task>')
