import os
import hashlib
from config import ALLOWED_EXTENSIONS

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
