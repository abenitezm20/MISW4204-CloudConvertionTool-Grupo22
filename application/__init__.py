from flask import Flask
from config import DATABASE_URI, REDIS
from .celery_utils import celery_init_app
from helper import encrypt

from modelos import db, Tarea, Usuario

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_mapping(
        CELERY=dict(
            broker_url=REDIS,
            result_backend=REDIS
        ),
    )

    db.init_app(app)

    celery = celery_init_app(app)
    celery.set_default()

    return app, celery