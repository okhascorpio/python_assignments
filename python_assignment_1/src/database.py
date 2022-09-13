#
# Handels everything related to the postgresql database
#


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db= SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True )
    password = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    todos = db.relationship('Todos')


# status of type enum for the todo items in the database
class STATUS(str,Enum):
   NotStarted = 'NotStarted'
   OnGoing = 'OnGoing'
   Completed = 'Completed'

   @classmethod
   def has_key(cls,key):
    return key in cls.__members__



class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String())
    description = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Enum(STATUS), default=STATUS.NotStarted)


# END