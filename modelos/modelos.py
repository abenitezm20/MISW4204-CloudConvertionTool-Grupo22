import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Enum

db = SQLAlchemy()


class StatusEnum(str, enum.Enum):
    uploaded = "uploaded"
    processed = "processed"


class NewFormatEnum(str, enum.Enum):
    ZIP = "ZIP"
    TAR_GZ = "TAR.GZ"
    TAR_BZ2 = "TAR.BZ2"


class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(512))
    newFormat = db.Column(db.String(10))
    timeStamp = db.Column(db.DateTime)
    status = db.Column(Enum(StatusEnum))


class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships = True
        load_instance = True
