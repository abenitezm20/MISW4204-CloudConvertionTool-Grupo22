import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from modelos import db, Tarea, Usuario
from vistas import Tareas, GestionTareas, Health, GestionArchivos
from helper import encrypt

DATABASE_URI = os.environ.get(
    'DATABASE_URI') or 'postgresql://admin:admin@localhost:5432/tool'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

with app_context:
    Tarea.query.delete()
    Usuario.query.delete()
    usuario1=Usuario(usuario='alexanderB' , contrasena=encrypt('alexander') , email='alexanderB@uniandes.edu.co')
    usuario2=Usuario(usuario='danielO' , contrasena=encrypt('daniel') , email='danielO@uniandes.edu.co')
    usuario3=Usuario(usuario='lauraC' , contrasena=encrypt('laura') , email='lauraC@uniandes.edu.co')
    usuario4=Usuario(usuario='alexanderC' , contrasena=encrypt('alexander') , email='alexanderC@uniandes.edu.co')
    db.session.add_all([usuario1,usuario2,usuario3,usuario4])
    db.session.commit()

cors = CORS(app)

api = Api(app)
api.add_resource(Tareas, '/api/tasks')
api.add_resource(GestionTareas, '/api/tasks/<int:id_task>')
api.add_resource(GestionArchivos, '/api/files/<filename>')
api.add_resource(Health, '/health')
