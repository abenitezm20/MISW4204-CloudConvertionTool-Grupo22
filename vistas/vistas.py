import os
import datetime
import json
import redis
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from modelos import db, StatusEnum, NewFormatEnum, Tarea, TareaSchema


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}

CANAL_TAREAS = 'tareas'
REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_DB = os.environ.get('REDIS_DB') or 0
REDIS_CONNECTION = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
redis_db = REDIS_CONNECTION

tarea_schema = TareaSchema()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_file_path(filename):
    base_path = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    return os.path.join(base_path, filename)


class Tareas(Resource):

    def get(self):
        tareas = Tarea.query.all()
        return [tarea_schema.dump(tarea) for tarea in tareas]

    def post(self):
        if 'file' not in request.files:
            return 'El archivo es obligatorio', 400

        file = request.files['file']

        if file.filename == '':
            return 'Debe seleccionar un archivo con un nombre válido', 400

        if request.form['newFormat'] == '':
            return 'El formato para la conversión es obligatorio', 400

        new_format = request.form['newFormat']
        if new_format not in [formato.value for formato in NewFormatEnum]:
            return 'Formato no soportado', 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Almacena el archivo en disco
            upload_path = get_upload_file_path(filename)
            file.save(upload_path)

            # Registra la tarea en BD
            tarea = Tarea(fileName=file.filename, newFormat=new_format,
                          timeStamp=datetime.datetime.now(), status=StatusEnum.uploaded)
            db.session.add(tarea)

            # Publica tarea pendiente
            redis_db.publish(CANAL_TAREAS, json.dumps(
                tarea_schema.dump(tarea)))

            # Finaliza transacción
            db.session.commit()
            return 'Tarea creada - {}'.format(tarea.id), 200

        return 'Extensión del archivo no permitido', 400


class GestionTareas(Resource):

    def get(self, id_task):
        return tarea_schema.dump(Tarea.query.get_or_404(id_task, 'Tarea no encontrada'))

    def delete(self, id_task):
        tarea = Tarea.query.get_or_404(id_task, 'Tarea no encontrada')
        db.session.delete(tarea)
        db.session.commit()
        return '', 204

class Health(Resource):

    def get(self):
        return 'OK', 200
