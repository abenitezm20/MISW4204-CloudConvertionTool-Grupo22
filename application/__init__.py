from flask import Flask
from config import DATABASE_URI, REDIS
from .celery_utils import celery_init_app
from datetime import timedelta
from modelos import db

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=10)
    app.config['JWT_SECRET_KEY'] = 'supersecret'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1014 * 1024 # 16Mb

    db.init_app(app)

    app.config.from_mapping(
        CELERY=dict(
            broker_url=REDIS,
            result_backend=REDIS
        ),
    )
    celery = celery_init_app(app)
    celery.set_default()
    
    return app, celery