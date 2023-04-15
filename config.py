import os

REDIS = "redis://redis"
STATIC_FOLDER = os.path.join(os.getcwd(), 'files/static/')
MEDIA_FOLDER = os.path.join(os.getcwd(), 'files/media/')
DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://admin:admin@localhost:5432/tool'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}