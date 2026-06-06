# ADR 001: Gestão de Configuração e Segurança com Variáveis de Ambiente

**Data**: 2026-06-06  
**Status**: Aceito  
**Contexto**: Projeto Flask para gerenciamento de tarefas  

## Problema

A aplicação tinha configurações sensíveis (SECRET_KEY) hardcoded no código-fonte, causando:
- ⚠️ Exposição de credenciais em repositório Git
- ⚠️ Impossibilidade de ter configurações diferentes por ambiente
- ⚠️ Violação de OWASP A02:2021 – Cryptographic Failures
- ⚠️ Dificuldade em deploy em produção seguro

## Solução

Implementar gestão centralizada de configuração via **variáveis de ambiente** usando `python-dotenv`:

### Mudanças Realizadas

#### 1. **Arquivo `.env` (Local, Ignorado no Git)**
```python
# .env (NÃO versionado)
SECRET_KEY=3e81aeb3013681d92cdd9de78284b2e36113f12201d8f843de5a696ef88bdd07
DATABASE_URL=sqlite:///site.db
FLASK_ENV=development
```

#### 2. **Arquivo `.env.example` (Versionado)**
```python
# .env.example (para o repositório)
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///site.db
FLASK_ENV=development
```

#### 3. **Atualização `config.py`**
```python
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-only')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SESSION_COOKIE_SECURE = False  # True em produção
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

#### 4. **Flags de Segurança de Sessão**
Adicionadas em `ProductionConfig`:
```python
SESSION_COOKIE_SECURE = True        # HTTPS only
SESSION_COOKIE_HTTPONLY = True      # Bloqueia JS access
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection mais restritiva
```

#### 5. **Type Hints e Documentação**
```python
def create_app(config_name: str = 'development') -> Flask:
    """Factory com type hints completos e logging."""
```

#### 6. **Tratamento de Erros e Logging**
```python
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    logger.error(f"Erro ao criar tabelas: {e}")
    raise
```

## Consequências

### ✅ Benefícios
- 🔒 Segurança: Credenciais fora do repositório
- 🔄 Flexibilidade: Diferentes configs por ambiente (dev/prod/test)
- 📋 Rastreabilidade: Logging centralizado de eventos
- 🛡️ Compliance: OWASP A02 + session cookies seguras
- 🧪 Testabilidade: Factory pattern + type hints
- 📚 Documentação: Comentários detalhados em cada linha

### ⚠️ Tradeoffs
- Desenvolvedores precisam copiar `.env.example` para `.env` (mitigado com SETUP.md)
- Necessidade de `python-dotenv` como dependência (menor, bem mantida)

## Alternativas Consideradas

1. **Variáveis de ambiente do SO** ❌ Mais complexo para desenvolvimento local
2. **Arquivo `local.py` gitignored** ❌ Menos padrão, sem exemplo template
3. **Secrets manager (Vault)** ❌ Overkill para projeto inicial
4. **Config em banco de dados** ❌ Chicken-and-egg problem

## Referências

- [OWASP A02:2021 – Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Flask Configuration Best Practices](https://flask.palletsprojects.com/config/)
- [Session Security in Flask](https://flask.palletsprojects.com/en/2.3.x/security/#sessions)

## Próximos Passos

1. ✅ Atualizar `requirements.txt` com `python-dotenv`
2. ✅ Criar `SETUP.md` com instruções de configuração
3. ⏳ Implementar `.env` automático em CI/CD
4. ⏳ Adicionar validação de variáveis obrigatórias no startup
5. ⏳ Implementar rate limiting e mais proteções de segurança
