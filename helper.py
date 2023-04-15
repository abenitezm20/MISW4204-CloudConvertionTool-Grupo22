import os
import hashlib
import zipfile
from os.path import basename
from modelos import db, Tarea, NewFormatEnum, StatusEnum

STATIC_FOLDER = os.path.join(os.getcwd(), 'files/static/')
MEDIA_FOLDER = os.path.join(os.getcwd(), 'files/media/')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}

def encrypt(text):
    text = text.encode('utf-8')
    return hashlib.md5(text).hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_path(filename, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return os.path.join(folder, filename)

def filepath(filename, folder):
    return os.path.join(folder, filename)

def compress_file(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    filename = tarea.fileName
    filename_no_ext = filename.split('.')[0]
    ext = tarea.newFormat
    if ext == NewFormatEnum.ZIP:
        zip_file(filename, filename_no_ext, ext)
        update_task_state(tarea, StatusEnum.processed)


def zip_file(filename, filename_no_ext, new_ext):
    original_filepath = filepath(filename, MEDIA_FOLDER)
    new_filename = f"{filename_no_ext}.{new_ext}"
    new_filepath = get_file_path(new_filename, STATIC_FOLDER)
    with zipfile.ZipFile(new_filepath, 'w') as f:
        f.write(original_filepath, basename(original_filepath))

def update_task_state(tarea, state):
    tarea.status = state
    db.session.add(tarea)
    db.session.commit()
