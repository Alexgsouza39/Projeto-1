# Guia de Segurança - Projeto-1

Boas práticas de segurança e configuração para desenvolvimento e produção.

---

## 🔒 Segurança de Credenciais

### DON'T ❌
```python
# NUNCA faça isso
SECRET_KEY = 'minha-chave-secreta'
DB_PASSWORD = 'admin123'
API_TOKEN = 'sk_live_...'
```

### DO ✅
```python
# Use .env (local) para desenvolvimento
# .env (GITIGNORED - local apenas)
SECRET_KEY=gera-com-secrets-token-hex-32
DB_PASSWORD=leia-do-.env

# Use variáveis de ambiente em produção
import os
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY nao configurada!")
```

---

## 🌍 Configuração por Ambiente

### Desenvolvimento (`config_name='development'`)
```python
DEBUG = True                        # Ativa debug mode
SESSION_COOKIE_SECURE = False       # HTTP allowed
SESSION_COOKIE_SAMESITE = 'Lax'    # Menos restritivo
TESTING = False
```

**Setup**:
```bash
cp .env.example .env
# Edite .env com valores de desenvolvimento
python app.py
```

### Produção (`config_name='production'`)
```python
DEBUG = False                       # NUNCA True em prod!
SESSION_COOKIE_SECURE = True        # HTTPS only
SESSION_COOKIE_SAMESITE = 'Strict'  # Máxima segurança
TESTING = False
```

**Setup**:
```bash
# Gere nova chave
python -c "import secrets; print(secrets.token_hex(32))"

# Configure em .env ou variáveis do SO
export SECRET_KEY=<nova-chave>
export DATABASE_URL=postgresql://...
export FLASK_ENV=production

# Execute com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Testes (`config_name='testing'`)
```python
TESTING = True                      # Ativa modo teste
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Banco em memória
WTF_CSRF_ENABLED = False           # Desativa CSRF para testes
```

---

## 🔑 Gestão de Secrets

### Gerar SECRET_KEY
```bash
# Opção 1: Python secrets
python -c "import secrets; print(secrets.token_hex(32))"

# Opção 2: OpenSSL
openssl rand -hex 32

# Copie a saída para .env
SECRET_KEY=3e81aeb3013681d92cdd9de78284b2e36113f12201d8f843de5a696ef88bdd07
```

### Validar Secrets no Startup
```python
# Em app.py ou config.py
def validate_config():
    required_vars = ['SECRET_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Variaveis obrigatorias nao configuradas: {missing}")

# Chamar no create_app()
validate_config()
```

---

## 🍪 Session Cookie Security

### HTTPONLY (Protege contra XSS)
```python
SESSION_COOKIE_HTTPONLY = True
```
**Efeito**: JavaScript não consegue acessar `document.cookie`  
**Mitiga**: Cross-Site Scripting (XSS) attacks

### SAMESITE (Protege contra CSRF)
```python
# Desenvolvimento
SESSION_COOKIE_SAMESITE = 'Lax'     # Permite get requests inter-site

# Produção
SESSION_COOKIE_SAMESITE = 'Strict'  # Bloqueia tudo inter-site
```
**Efeito**: Restringe quando cookies são enviados  
**Mitiga**: Cross-Site Request Forgery (CSRF) attacks

### SECURE (Força HTTPS)
```python
SESSION_COOKIE_SECURE = True
```
**Efeito**: Cookie só é enviado em conexões HTTPS  
**Mitiga**: Man-in-the-Middle (MITM) attacks

---

## 🚨 Checklist de Segurança antes de Deploy

### Código
- [ ] Nenhum `print()` com dados sensíveis em produção
- [ ] Logging não expõe passwords/tokens
- [ ] Validação de input em todas as rotas
- [ ] Tratamento de erros sem stack traces em produção

### Configuração
- [ ] `DEBUG = False` em produção
- [ ] `SECRET_KEY` é diferente do desenvolvimento
- [ ] `DATABASE_URL` aponta para banco seguro (não SQLite)
- [ ] Todas as variáveis obrigatórias estão configuradas

### Segurança
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_HTTPONLY = True`
- [ ] `SESSION_COOKIE_SAMESITE = 'Strict'`
- [ ] CSRF Protection ativado (`WTF_CSRF_ENABLED = True`)
- [ ] HTTPS configurado no servidor

### Logs e Monitoramento
- [ ] Logging ativado
- [ ] Logs não são acessíveis publicamente
- [ ] Monitoramento de erros configurado (Sentry, etc)
- [ ] Alertas para valores anómalos

### Dependências
- [ ] Todas as dependências têm versões pinadas
- [ ] Nenhuma dependência com vulnerabilidades conhecidas
- [ ] `pip audit` rodou sem problemas

---

## 🔗 Links de Segurança

### OWASP Top 10 2021
- [A01:2021 - Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [A02:2021 - Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [A03:2021 - Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [A05:2021 - Cross-Site Request Forgery](https://owasp.org/Top10/A05_2021-Cross-Site_Request_Forgery/)
- [A06:2021 - Security Misconfiguration](https://owasp.org/Top10/A06_2021-Security_Misconfiguration/)

### Flask Security
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Session Interface](https://flask.palletsprojects.com/en/2.3.x/api/#flask.sessions.SessionInterface)
- [CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf/)

### Criptografia
- [Python secrets Module](https://docs.python.org/3/library/secrets.html)
- [NIST Guidelines](https://pages.nist.gov/800-63-3/)

---

## 🎯 Resumo Rápido

**DON'T EVER**:
- [ ] Commitar `.env` com secrets reais
- [ ] Deixar `DEBUG=True` em produção
- [ ] Usar SQLite em produção com múltiplos usuários
- [ ] Compartilhar `SECRET_KEY` entre ambientes
- [ ] Expor stack traces em responses de erro

**ALWAYS**:
- [ ] Usar `.env` para desenvolvimento
- [ ] Gerar nova `SECRET_KEY` para cada ambiente
- [ ] Usar variáveis de ambiente em produção
- [ ] Ativar session cookie flags de segurança
- [ ] Fazer audit de dependências regularmente

---

**Versão**: 1.0  
**Data**: 2026-06-06  
**Atualizado por**: Senior Fullstack Developer
