"""
app.py
------
Aplicação principal Flask para gerenciamento de tarefas e subtarefas.
Inclui autenticação, cadastro, visualização, conclusão e exclusão de tarefas.

Arquitetura em camadas:
- models/ : Modelos de banco de dados
- routes/ : Rotas (blueprints)
- services/ : Lógica de negócio
- utils/ : Utilitários
- config.py : Configurações
- forms.py : Validações de formulários
"""
import os
from flask import Flask
from flask_wtf import CSRFProtect
from config import config
from models import init_models
from routes import register_routes


def create_app(config_name='development'):
    """
    Factory para criar a aplicação Flask.
    
    Args:
        config_name: Nome da configuração ('development', 'production', 'testing')
    
    Returns:
        Flask: Instância da aplicação
    """
    app = Flask(__name__)
    
    # Carrega configurações
    app.config.from_object(config[config_name])
    
    # Inicializa extensões
    csrf = CSRFProtect(app)
    db = init_models(app)
    
    # Registra rotas
    register_routes(app)
    
    # Favicon
    @app.route('/favicon.ico')
    def favicon():
        from flask import send_from_directory
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    
    # Cria tabelas
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
