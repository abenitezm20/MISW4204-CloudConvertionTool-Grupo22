from celery import shared_task
from modelos import db, Tarea, NewFormatEnum, StatusEnum
import zipfile
from os.path import basename
from helper import filepath, get_file_path, get_static_folder_by_user

@shared_task(bind=True)
def compress_file(self, tarea_id):
    tarea = Tarea.query.get(tarea_id)
    filename = tarea.fileName
    user_id = tarea.user_id
    ext = tarea.newFormat
    origin, destination = get_origin_destination_paths(user_id, filename, ext)
    if ext == NewFormatEnum.ZIP:
        zip_file(origin, destination)
        update_task_state(tarea, StatusEnum.processed)


def zip_file(original_path, destination_path):
    with zipfile.ZipFile(destination_path, 'w') as f:
        f.write(original_path, basename(original_path))

def get_origin_destination_paths(user_id, filename, new_ext):
    filename_no_ext = filename.split('.')[0]
    print('file no ext: ', filename_no_ext)
    user_path = get_static_folder_by_user(user_id)
    print('user_path: ', user_path)
    original_filepath = filepath(filename, user_path)
    print('original path: ', original_filepath)
    new_filename = f"{filename_no_ext}.{new_ext}"
    print('filename: ', new_filename)
    new_filepath = get_file_path(new_filename, user_path)
    print(' new filepath: ', new_filepath)
    return original_filepath, new_filepath

def update_task_state(tarea, state):
    tarea.status = state
    db.session.add(tarea)
    db.session.commit()