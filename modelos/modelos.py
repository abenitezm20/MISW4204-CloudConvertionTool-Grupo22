import enum
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Enum

class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

db = SQLAlchemy()

class StatusEnum(str, enum.Enum):
    uploaded = "uploaded"
    processed = "processed"

class NewFormatEnum(str, enum.Enum):
    ZIP = "zip"
    TAR_GZ = "tar.gz"
    TAR_BZ2 = "tar.bz2"

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True)
    contrasena = db.Column(db.String(50))
    email = db.Column(db.String(30), unique=True)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    fileName = db.Column(db.String(512))
    newFormat = db.Column(db.String(10))
    createdAt = db.Column(db.DateTime)
    processTime = db.Column(db.Float(precision=3), nullable=True)
    status = db.Column(Enum(StatusEnum))

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships = True
        load_instance = True
