"""
models/subtask.py
-----------------
Modelo de subtarefa vinculada a uma tarefa principal.
"""
from . import db


class Subtask(db.Model):
    """Modelo de subtarefa vinculada a uma tarefa principal."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completion_date = db.Column(db.String(20), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
