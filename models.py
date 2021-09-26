import pymysql
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


pymysql.install_as_MySQLdb()
db = SQLAlchemy()

# 基本模型
class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # isDelete=db.Column(db.Boolean,default=False)
    # e = db.Column(db.Enum('python', 'flask'))

    def to_dict(self):
        result = {}
        for c in self.__table__.columns:
            name = c.name
            value = getattr(self, name, None)
            if type(value) == datetime:
                value = value.strftime("%Y-%m-%d %H:%M:%S")

            result[name] = value

        return result


class User(db.Model, BaseModel):
    __tablename__ = 'user'