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
- config.py : Configurações com suporte a variáveis de ambiente
- forms.py : Validações de formulários
"""
import os
import logging
from typing import Optional
from flask import Flask
from flask_wtf import CSRFProtect
from config import config
from models import init_models
from routes import register_routes

# Configuração de logging para rastreamento de eventos
logger = logging.getLogger(__name__)


def create_app(config_name: str = 'development') -> Flask:
    """
    Factory para criar a aplicação Flask com toda a stack configurada.
    
    Este padrão permite:
    - Múltiplas instâncias com configurações diferentes
    - Testes isolados com configuração de teste
    - Injeção de dependências via config_name
    
    Args:
        config_name (str): Nome da configuração
            - 'development': Debug ativado, HTTPS não obrigatório
            - 'production': Debug desativado, HTTPS obrigatório
            - 'testing': Usa banco em memória, CSRF desativado
    
    Returns:
        Flask: Instância da aplicação configurada e pronta para uso
    
    Raises:
        ValueError: Se config_name não for válido
        Exception: Se houver erro ao criar tabelas no banco de dados
    """
    # Valida se a configuração solicitada existe
    if config_name not in config:
        raise ValueError(
            f"Configuração inválida: '{config_name}'. "
            f"Opções válidas: {list(config.keys())}"
        )
    
    # Registra início da criação da aplicação
    logger.info(f"Criando aplicação Flask com configuração: {config_name}")
    
    # Instancia a aplicação Flask
    app = Flask(__name__)
    
    # Carrega configurações específicas do ambiente
    # Integra variáveis do .env através de config.py
    app.config.from_object(config[config_name])
    logger.debug(f"Configuração carregada de: {config[config_name].__name__}")
    
    # Inicializa extensões de segurança
    # CSRFProtect protege contra ataques CSRF em formulários
    try:
        csrf = CSRFProtect(app)
        logger.debug("CSRF Protection ativada")
    except Exception as e:
        logger.error(f"Erro ao inicializar CSRF Protection: {e}")
        raise
    
    # Inicializa ORM SQLAlchemy para acesso ao banco de dados
    try:
        db = init_models(app)
        logger.debug("Modelos de banco de dados inicializados")
    except Exception as e:
        logger.error(f"Erro ao inicializar modelos: {e}")
        raise
    
    # Registra todos os blueprints de rotas da aplicação
    try:
        register_routes(app)
        logger.debug("Rotas registradas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao registrar rotas: {e}")
        raise
    
    # Rota para servir favicon.ico (ícone da ababa do navegador)
    @app.route('/favicon.ico')
    def favicon():
        """
        Retorna o favicon da aplicação.
        Reduz erros 404 no navegador ao buscar favicon automaticamente.
        """
        from flask import send_from_directory
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    
    # Cria tabelas do banco de dados se não existirem
    # Usa contexto de aplicação para operações de banco
    try:
        with app.app_context():
            logger.info(f"Criando tabelas no banco: {app.config['SQLALCHEMY_DATABASE_URI']}")
            db.create_all()
            logger.info("Tabelas criadas/verificadas com sucesso")
    except Exception as e:
        logger.error(f"Erro crítico ao criar tabelas: {e}")
        raise
    
    logger.info(f"Aplicação criada com sucesso em modo: {config_name}")
    return app


if __name__ == '__main__':
    """
    Ponto de entrada da aplicação.
    Executa em modo desenvolvimento por padrão.
    Use a variável FLASK_ENV para mudar de ambiente.
    """
    # Configura logging para ver eventos no console durante desenvolvimento
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Cria aplicação com configuração de desenvolvimento
        app = create_app('development')
        
        # Executa servidor de desenvolvimento
        # debug=True: recarrega automaticamente ao salvar arquivos
        # use_reloader=True: reinicia ao detectar mudanças
        logger.info("Iniciando servidor Flask em http://127.0.0.1:5000")
        app.run(debug=True, use_reloader=True)
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {e}", exc_info=True)
        raise
