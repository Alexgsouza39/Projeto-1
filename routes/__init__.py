"""
routes/__init__.py
------------------
Inicialização das rotas (blueprints).
"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
tasks_bp = Blueprint('tasks', __name__)


def register_routes(app):
    """Registra todos os blueprints na aplicação."""
    import routes.auth
    import routes.tasks
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
