from celery import shared_task
from modelos import db, Tarea, NewFormatEnum, StatusEnum
import zipfile
from os.path import basename
from helper import filepath, get_file_path
from config import MEDIA_FOLDER, STATIC_FOLDER

@shared_task(bind=True)
def compress_file(self, tarea_id):
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