"""
config.py
---------
Configurações centralizadas da aplicação Flask.
Carrega variáveis de ambiente de .env para melhor segurança.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Carrega variáveis de .env no contexto
load_dotenv()


class Config:
    """
    Configuração base da aplicação.
    
    Atributos:
        SECRET_KEY (str): Chave para criptografia de sessão e CSRF
        SQLALCHEMY_DATABASE_URI (str): URI de conexão com o banco de dados
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Desativa tracking automático de modificações
        PERMANENT_SESSION_LIFETIME (timedelta): Tempo de vida da sessão persistente
        WTF_CSRF_ENABLED (bool): Ativa proteção CSRF com Flask-WTF
        SESSION_COOKIE_SECURE (bool): HTTPS only (ativado em produção)
        SESSION_COOKIE_HTTPONLY (bool): Bloqueia acesso JS aos cookies
        SESSION_COOKIE_SAMESITE (str): Proteção contra CSRF por cookie
    """
    # Lê SECRET_KEY do .env, com fallback apenas para desenvolvimento
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Lê URI de banco de dados do .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    
    # Desativa tracking automático para melhor performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Define tempo máximo de sessão persistente (30 minutos)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Ativa proteção CSRF com Flask-WTF
    WTF_CSRF_ENABLED = True
    
    # Flags de segurança de cookies (desenvolvidos aqui, ativados em produção)
    SESSION_COOKIE_SECURE = False  # Será True em produção (HTTPS only)
    SESSION_COOKIE_HTTPONLY = True  # Bloqueia acesso via JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'  # Proteção contra CSRF


class DevelopmentConfig(Config):
    """
    Configuração de desenvolvimento.
    
    Ativa debug mode para melhor experiência de desenvolvimento.
    Cookies não requerem HTTPS (apenas localhost).
    """
    DEBUG = True
    # Em desenvolvimento, não requer HTTPS
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """
    Configuração de produção.
    
    Desativa debug, ativa flags de segurança e requer HTTPS.
    Recomenda-se usar PostgreSQL ou MySQL em produção.
    """
    DEBUG = False
    # Em produção, cookies apenas por HTTPS (segurança obrigatória)
    SESSION_COOKIE_SECURE = True
    # Validação mais restritiva de SameSite em produção
    SESSION_COOKIE_SAMESITE = 'Strict'


class TestingConfig(Config):
    """
    Configuração de testes.
    
    Usa banco de dados em memória para testes rápidos e isolados.
    Desativa CSRF para simplificar testes de formulário.
    """
    TESTING = True
    # Usa banco de dados em memória para testes (rápido e isolado)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Desativa CSRF em testes para facilitar submissões de formulário
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
