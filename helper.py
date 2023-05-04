import os
import hashlib
import re
from config import ALLOWED_EXTENSIONS, STATIC_FOLDER
from random import randint

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

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

def is_email(email):
    resultado = re.fullmatch(regex, email)
    print(resultado)
    if resultado:
        return True
    
    return False

def get_static_folder_by_user(user_id):
    user_id = str(user_id)
    user_path = f'{STATIC_FOLDER}'
    return os.path.join(os.getcwd(), user_path)

def random_int(n=8):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        
