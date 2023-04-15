import datetime
from flask import request, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename
from helper import allowed_file, get_file_path, is_email, encrypt, get_static_folder_by_user
from config import REGISTER_ALLOWED_FIELDS
from tasks import compress_file
from sqlalchemy import exc
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from modelos import db, StatusEnum, NewFormatEnum, Tarea, TareaSchema, Usuario

tarea_schema = TareaSchema()

class Registrar(Resource):

    def post(self):
        datos = request.get_json()
        for field in REGISTER_ALLOWED_FIELDS:
            if field not in datos:
                return f'el campo {field} es obligatorio', 422
            
            if datos[field] == '' or datos[field] is None:
                return f"el campo {field} no puede estar vacio", 422
            
        if datos['password1'] != datos['password2']:
            return "la contrasena no coincide"
        
        if not is_email(datos['email']):
            return "el correo no tiene un formato valido"
        
        try:
            usuario = Usuario(usuario=datos['username'], contrasena=encrypt(datos['password1']), email=datos['email'])
            db.session.add(usuario)
            db.session.commit()
        except exc.IntegrityError:
            return 'el campo username o email ya se encuentra registrado', 400

        return 'usuario creado exitosamente'
        
class Autenticar(Resource):

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if username is None or password is None:
            return 'No se permiten campos vacios', 422
        
        usuario = Usuario.query.filter(Usuario.usuario==username, Usuario.contrasena==encrypt(password)).first()
        if usuario is None:
            return 'usuario no encontrado'
        
        token = create_access_token(identity=usuario.id)

        return {'token': token}

class Tareas(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        tareas = Tarea.query.filter(Tarea.user_id==user_id).all()
        return [tarea_schema.dump(tarea) for tarea in tareas]

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if 'file' not in request.files:
            return 'El archivo es obligatorio', 400

        file = request.files['file']
        new_format = request.form['newFormat']

        if file.filename == '':
            return 'Debe seleccionar un archivo con un nombre válido', 400

        if new_format == '':
            return 'El formato para la conversión es obligatorio', 400

        if new_format not in [formato.value for formato in NewFormatEnum]:
            return f"El formato {new_format} para la conversión no es soportado", 400
        
        if not allowed_file(file.filename):
            return 'El formato del archivo no es soportado', 400

        filename = secure_filename(file.filename)
        # Almacena el archivo en disco
        file_path_by_user = get_static_folder_by_user(user_id)
        upload_path = get_file_path(filename, file_path_by_user)
        file.save(upload_path)

        # Registra la tarea en BD
        tarea = Tarea(fileName=filename, newFormat=new_format, user_id=user_id,
                        timeStamp=datetime.datetime.now(), status=StatusEnum.uploaded)
        db.session.add(tarea)
        db.session.commit()

        compress_file.delay(tarea.id)
        return 'Tarea creada - {}'.format(tarea.id), 200


class GestionTareas(Resource):

    def get(self, id_task):
        return tarea_schema.dump(Tarea.query.get_or_404(id_task, 'Tarea no encontrada'))

    def delete(self, id_task):
        tarea = Tarea.query.get_or_404(id_task, 'Tarea no encontrada')
        db.session.delete(tarea)
        db.session.commit()
        return '', 204
    
class GestionArchivos(Resource):

    @jwt_required()
    def get(self, filename):
        print('filename: ', filename)
        user_id = get_jwt_identity()
        file_path_by_user = get_static_folder_by_user(user_id)
        return send_from_directory(file_path_by_user, filename)
    


class Health(Resource):

    def get(self):
        return 'OK', 200
