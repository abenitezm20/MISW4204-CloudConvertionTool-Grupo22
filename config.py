import os

REDIS = "redis://redis"
STATIC_FOLDER = 'files/static/'
DATABASE_URI = os.environ.get('DATABASE_URI')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}
REGISTER_ALLOWED_FIELDS = ['username', 'password1', 'password2', 'email']