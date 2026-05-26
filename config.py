"""
config.py
---------
Configurações centralizadas da aplicação Flask.
"""
from datetime import timedelta


class Config:
    """Configuração base da aplicação."""
    SECRET_KEY = 'Meu_App_Secreto'  # Troque por uma chave forte em produção
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuração de produção."""
    DEBUG = False


class TestingConfig(Config):
    """Configuração de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
