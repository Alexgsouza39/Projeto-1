"""
models/__init__.py
------------------
Inicialização de modelos e banco de dados.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_models(app):
    """Inicializa os modelos com a aplicação."""
    from .user import User
    from .task import Task
    from .subtask import Subtask
    
    db.init_app(app)
    return db
