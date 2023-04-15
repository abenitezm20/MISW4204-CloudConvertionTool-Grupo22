import os
import datetime
import json
import redis
from flask import request, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename
from helper import allowed_file, get_file_path, STATIC_FOLDER, MEDIA_FOLDER, compress_file

from modelos import db, StatusEnum, NewFormatEnum, Tarea, TareaSchema

CANAL_TAREAS = 'tareas'
REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_DB = os.environ.get('REDIS_DB') or 0
REDIS_CONNECTION = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
redis_db = REDIS_CONNECTION

tarea_schema = TareaSchema()

class Tareas(Resource):

    def get(self):
        tareas = Tarea.query.all()
        return [tarea_schema.dump(tarea) for tarea in tareas]

    def post(self):
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
        upload_path = get_file_path(filename, MEDIA_FOLDER)
        file.save(upload_path)

        # Registra la tarea en BD
        tarea = Tarea(fileName=file.filename, newFormat=new_format,
                        timeStamp=datetime.datetime.now(), status=StatusEnum.uploaded)
        db.session.add(tarea)
        db.session.commit()

        compress_file(tarea.id)
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

    def get(self, filename):
        return send_from_directory(STATIC_FOLDER, filename)


class Health(Resource):

    def get(self):
        return 'OK', 200
