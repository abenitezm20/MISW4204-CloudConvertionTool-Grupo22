import os

REDIS = "redis://redis"
# REDIS = "redis://127.0.0.1:6379"
STATIC_FOLDER = 'files/static/'
DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://admin:admin@localhost:5432/tool'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}
REGISTER_ALLOWED_FIELDS = ['username', 'password1', 'password2', 'email']