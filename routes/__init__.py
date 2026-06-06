"""
routes/__init__.py
------------------
Inicialização e registro de rotas (blueprints).

Bluaprints são módulos reutilizáveis de rotas que separam preocupações:
- auth_bp: Autenticação (login, registro, logout)
- tasks_bp: Gerenciamento de tarefas (CRUD)
"""
from typing import Optional
from flask import Flask, Blueprint

# Blueprint para rotas de autenticação
# Grupo lógico: login, registro, logout, reset de senha
auth_bp: Blueprint = Blueprint('auth', __name__)

# Blueprint para rotas de gerenciamento de tarefas
# Grupo lógico: criar, listar, editar, deletar tarefas
tasks_bp: Blueprint = Blueprint('tasks', __name__)


def register_routes(app: Flask) -> None:
    """
    Registra todos os blueprints (módulos de rotas) na aplicação.
    
    Esta função centraliza o registro de todas as rotas, facilitando:
    - Manutenção: mudanças em um lugar apenas
    - Descoberta: ver todas as rotas registradas
    - Flexibilidade: registrar blueprints condicionalmente se necessário
    
    Args:
        app (Flask): Instância da aplicação Flask onde registrar os blueprints
    
    Returns:
        None
    
    Exemplo:
        app = Flask(__name__)
        register_routes(app)  # Registra auth_bp e tasks_bp
    """
    # Importa módulos de rotas para carregar suas definições
    # As importações devem estar aqui para evitar importações circulares
    import routes.auth
    import routes.tasks
    
    # Registra blueprint de autenticação na aplicação
    # Pode adicionar url_prefix se desejar prefixar as rotas (ex: '/auth')
    app.register_blueprint(auth_bp)
    
    # Registra blueprint de tarefas na aplicação
    # Pode adicionar url_prefix se desejar prefixar as rotas (ex: '/tasks')
    app.register_blueprint(tasks_bp)
