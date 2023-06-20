from datetime import datetime
# from marshmallow_sqlalchemy import fields
from config import db, ma


class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    date_modified = db.Column(
        db.DateTime, default=None, onupdate=datetime.utcnow
    )
    created_by = db.Column(db.Integer, 
                           db.ForeignKey("user.id"),
                           nullable=False,
    )
    modified_by = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

