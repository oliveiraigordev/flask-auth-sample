from flask_login import UserMixin
from database import db


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
