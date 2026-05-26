"""
models/user.py
--------------
Modelo de usuário do sistema.
"""
from . import db


class User(db.Model):
    """Modelo de usuário do sistema."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')
