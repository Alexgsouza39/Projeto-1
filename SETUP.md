# Setup e Configuração - Projeto-1

Guia completo para configurar e executar o projeto em desenvolvimento, produção e testes.

## 📋 Requisitos

- **Python 3.8+**
- **pip** ou **pipenv**
- **Git**

## 🚀 Instalação Rápida (Desenvolvimento)

### 1. Clonar Repositório
```bash
git clone <repo-url>
cd Projeto-1
```

### 2. Criar Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env (deixar com valores default é OK para desenvolvimento)
# Windows: notepad .env
# macOS/Linux: nano .env
```

### 5. Executar Aplicação
```bash
python app.py
```

Acesse: **http://localhost:5000**

---

## 🔐 Configuração de Produção

### 1. Gerar Nova Secret Key
```bash
# IMPORTANTE: Usar uma chave diferente de desenvolvimento!
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie a saída.

### 2. Criar `.env` para Produção
```bash
SECRET_KEY=<cole-aqui-a-chave-gerada>
DATABASE_URL=postgresql://user:password@localhost/dbname
FLASK_ENV=production
FLASK_DEBUG=False
```

### 3. Instalar Banco de Dados (PostgreSQL recomendado)
```bash
# Instalar driver PostgreSQL
pip install psycopg2-binary

# Atualizar requirements.txt
pip freeze > requirements.txt
```

### 4. Usar Gunicorn para Produção
```bash
pip install gunicorn

# Executar com 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 5. Configurar HTTPS
- Use **Nginx** ou **Apache** como reverse proxy
- Configure certificado SSL/TLS (Let's Encrypt gratuito)
- As flags `SESSION_COOKIE_SECURE=True` serão ativadas automaticamente

---

## 🧪 Executar Testes

### Executar All Tests
```bash
pytest
```

### Executar com Cobertura
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Executar Um Arquivo Específico
```bash
pytest tests/test_auth.py -v
```

---

## 🛠️ Variáveis de Ambiente Disponíveis

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `SECRET_KEY` | `dev-secret-key-...` | Chave para criptografia de sessão e CSRF |
| `DATABASE_URL` | `sqlite:///site.db` | URI de conexão com banco de dados |
| `FLASK_ENV` | `development` | Ambiente: development, production, testing |
| `FLASK_DEBUG` | `True` | Ativar debug mode (nunca True em produção) |
| `FLASK_HOST` | `127.0.0.1` | Host para bind do servidor |
| `FLASK_PORT` | `5000` | Porta da aplicação |

---

## 📦 Estrutura do Projeto

```
Projeto-1/
├── app.py                 # Factory Flask + logging
├── config.py              # Configurações por ambiente
├── requirements.txt       # Dependências Python
├── .env                   # ⚠️ NÃO commitar (local apenas)
├── .env.example           # Template para .env
├── .gitignore             # Git ignore rules
├── models/
│   ├── __init__.py       # Init SQLAlchemy
│   ├── user.py           # Modelo User
│   ├── task.py           # Modelo Task
│   └── subtask.py        # Modelo Subtask
├── routes/
│   ├── __init__.py       # Registro de blueprints
│   ├── auth.py           # Rotas de auth
│   └── tasks.py          # Rotas de tasks
├── services/
│   ├── __init__.py
│   ├── auth_service.py   # Lógica de auth
│   ├── task_service.py   # Lógica de tasks
│   └── user_service.py   # Gerenciamento de user
├── templates/            # Templates HTML
├── static/               # CSS, JS, imagens
├── utils/                # Funções auxiliares
├── docs/
│   └── ADR-001-*.md      # Decisões arquiteturais
└── tests/               # Testes unitários
```

---

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "Database error: unable to open database file"
Certifique-se de que:
1. O diretório `instance/` existe (criado automaticamente)
2. Permissões de escrita no diretório do projeto

### "SECRET_KEY fallback-dev-only not found"
Confirme que `.env` foi criado a partir de `.env.example`:
```bash
cp .env.example .env
```

### Erro ao conectar PostgreSQL
Verifique:
1. PostgreSQL está rodando
2. `DATABASE_URL` está correto
3. Permissões de usuário/senha

---

## 📚 Recursos Adicionais

- [Flask Documentation](https://flask.palletsprojects.com)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [OWASP Security Guidelines](https://owasp.org/www-community/)

---

## 💡 Boas Práticas

✅ **Sempre fazer**:
- Copiar `.env.example` para `.env` ao clonar
- Usar virtual environment
- Commitar `.env.example`, NÃO `.env`
- Gerar nova SECRET_KEY para cada ambiente

❌ **Nunca fazer**:
- Commitar `.env` com secrets reais
- Usar SQLite em produção com múltiplos usuários
- Deixar `FLASK_DEBUG=True` em produção
- Compartilhar SECRET_KEY entre ambientes

---

**Versão**: 1.0  
**Última atualização**: 2026-06-06
