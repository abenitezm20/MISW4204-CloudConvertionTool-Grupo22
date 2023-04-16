from celery import shared_task
from modelos import db, Tarea, NewFormatEnum, StatusEnum
import zipfile
import tarfile
from os.path import basename
from helper import filepath, get_file_path, get_static_folder_by_user
from timeit import default_timer as timer

@shared_task(bind=True)
def compress_all(self):
    tareas = Tarea.query.filter(Tarea.status==StatusEnum.uploaded).all()
    for tarea in tareas:
        print(f"procesando tarea con id: {tarea.id}")
        compress_file(tarea)

def compress_file(tarea):
    filename = tarea.fileName
    user_id = tarea.user_id
    ext = tarea.newFormat
    origin, destination = get_origin_destination_paths(user_id, filename, ext)
    start_time = 0
    end_time = 0
    if ext == NewFormatEnum.ZIP:
        start_time = timer()
        zip_file(origin, destination)
        end_time = timer()
        update_task_state(start_time, end_time, tarea, StatusEnum.processed)
        return
    
    if ext == NewFormatEnum.TAR_GZ:
        start_time = timer()
        tar_gz(origin, destination)
        end_time = timer()
        update_task_state(start_time, end_time, tarea, StatusEnum.processed)
        return
    
    if ext == NewFormatEnum.TAR_BZ2:
        start_time = timer()
        tar_bz2(origin, destination)
        end_time = timer()
        update_task_state(start_time, end_time, tarea, StatusEnum.processed)
        return


def zip_file(original_path, destination_path):
    with zipfile.ZipFile(destination_path, 'w') as f:
        f.write(original_path, basename(original_path))

def tar_gz(original_path, destination_path):
    with tarfile.open(destination_path, 'w:gz') as tar:
        tar.add(original_path, arcname=basename(original_path))

def tar_bz2(original_path, destination_path):
    with tarfile.open(destination_path, 'w:bz2') as tar:
        tar.add(original_path, arcname=basename(original_path))

def get_origin_destination_paths(user_id, filename, new_ext):
    filename_no_ext = filename.split('.')[0]
    user_path = get_static_folder_by_user(user_id)
    original_filepath = filepath(filename, user_path)
    new_filename = f"{filename_no_ext}.{new_ext}"
    new_filepath = get_file_path(new_filename, user_path)
    return original_filepath, new_filepath

def update_task_state(start_time, end_time, tarea, state):
    tarea.status = state
    tarea.processTime = end_time - start_time
    db.session.add(tarea)
    db.session.commit()