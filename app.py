from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos import Tarea, Usuario
from vistas import db, Tareas, GestionTareas, Health, GestionArchivos, Registrar, Autenticar, Procesar
from helper import encrypt
from application import create_app

app, celery = create_app()
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)

db.create_all()

# with app_context:
#     Tarea.query.delete()
#     Usuario.query.delete()
#     usuario1=Usuario(usuario='alexanderB' , contrasena=encrypt('alexander') , email='alexanderB@uniandes.edu.co')
#     usuario2=Usuario(usuario='danielO' , contrasena=encrypt('daniel') , email='danielO@uniandes.edu.co')
#     usuario3=Usuario(usuario='lauraC' , contrasena=encrypt('laura') , email='lauraC@uniandes.edu.co')
#     usuario4=Usuario(usuario='alexanderC' , contrasena=encrypt('alexander') , email='alexanderC@uniandes.edu.co')
#     db.session.add_all([usuario1,usuario2,usuario3,usuario4])
#     db.session.commit()

cors = CORS(app)

api = Api(app)
api.add_resource(Registrar, '/api/auth/signup')
api.add_resource(Autenticar, '/api/auth/login')
api.add_resource(Tareas, '/api/tasks')
api.add_resource(GestionTareas, '/api/tasks/<int:id_task>')
api.add_resource(GestionArchivos, '/api/files/<filename>')
api.add_resource(Health, '/health')
api.add_resource(Procesar, '/procesar')