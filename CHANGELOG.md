# Changelog - Refatoração de Segurança e Arquitetura

## [1.1.0] - 2026-06-06

### 🔒 Segurança (CRÍTICO)

#### Secret Management
- **Antes**: `SECRET_KEY = 'Meu_App_Secreto'` hardcoded em `config.py`
- **Depois**: Leitura de `.env` via `python-dotenv`
  ```python
  SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-only')
  ```
- **Impacto**: Credenciais fora do repositório ✅

#### Session Cookies Seguras
- **Adicionado**: `SESSION_COOKIE_SECURE` = False (dev) / True (prod)
  - Força HTTPS em produção
- **Adicionado**: `SESSION_COOKIE_HTTPONLY` = True
  - Bloqueia acesso via JavaScript (protege contra XSS)
- **Adicionado**: `SESSION_COOKIE_SAMESITE` = 'Lax' (dev) / 'Strict' (prod)
  - Protege contra CSRF
- **Impacto**: Conformidade OWASP A06:2021 ✅

#### Variáveis de Ambiente
- **Novo**: `.env` (gitignored) com configurações locais
- **Novo**: `.env.example` para documentar vars obrigatórias
- **Novo**: `.gitignore` atualizado com `.env` e `*.db`
- **Impacto**: Diferentes configs por ambiente ✅

---

### 📝 Código e Documentação

#### Type Hints Completos
- **`app.py`**:
  ```python
  def create_app(config_name: str = 'development') -> Flask:
  ```
- **`routes/__init__.py`**:
  ```python
  def register_routes(app: Flask) -> None:
  ```
- **Impacto**: Melhor autocompletar IDE + type checking ✅

#### Logging Estruturado
- **Adicionado**: `import logging` e `logger = logging.getLogger(__name__)`
- **Eventos rastreados**:
  - Criação da aplicação
  - Inicialização de extensões
  - Criação de tabelas
  - Erros críticos
- **Impacto**: Facilita debugging e auditoria ✅

#### Tratamento de Erros Robusto
- **Novo**: Validação de `config_name` com mensagem clara
  ```python
  if config_name not in config:
      raise ValueError(f"Configuração inválida: '{config_name}'...")
  ```
- **Novo**: Try-except em todas as inicializações
  ```python
  try:
      csrf = CSRFProtect(app)
  except Exception as e:
      logger.error(f"Erro ao inicializar CSRF: {e}")
      raise
  ```
- **Impacto**: Falhas explícitas, não silenciosas ✅

#### Comentários Detalhados
- **Adicionado**: Docstrings expandidas em todas as funções
- **Adicionado**: Comentários inline explicando cada bloco
- **Exemplo**: `config.py` com explicação de cada flag
- **Impacto**: Onboarding mais fácil para novos devs ✅

---

### 🏗️ Arquitetura

#### Refinamento do Factory Pattern
- **Antes**: `create_app()` simples sem validação
- **Depois**: Factory robusto com:
  - Validação de config
  - Tratamento de erros
  - Logging de cada passo
  - Documentação completa
- **Impacto**: Mais confiável e testável ✅

#### Registro Centralizado de Blueprints
- **Refinado**: `register_routes()` com type hints
- **Adicionado**: Comentários sobre blueprint organization
- **Impacto**: Mais fácil adicionar novas rotas ✅

---

### 📚 Documentação

#### Novos Documentos
1. **`SETUP.md`** - Guia completo de instalação e configuração
   - Instalação rápida (dev)
   - Configuração de produção
   - Variáveis de ambiente
   - Troubleshooting

2. **`docs/ADR-001-gestao-configuracao-seguranca.md`** - Decision Record
   - Problema
   - Solução implementada
   - Consequências
   - Alternativas consideradas

3. **`requirements.txt`** - Atualizado com comentários
   - Seções: Core, Database, Security, Development, Production
   - Instruções para descomentar pacotes opcionais

---

### 📦 Dependências Adicionadas

```
python-dotenv==1.0.0      # Variáveis de ambiente
pytest==7.4.0             # Testes (novo)
pytest-cov==4.1.0         # Cobertura (novo)
```

**Instalação**: `pip install -r requirements.txt`

---

### ✅ Checklist de Implementação

- ✅ Gestão de secrets com `.env`
- ✅ Session cookies seguras
- ✅ Type hints completos
- ✅ Logging estruturado
- ✅ Tratamento de erros robusto
- ✅ Comentários detalhados
- ✅ Documentação profissional
- ✅ `.gitignore` atualizado
- ✅ `requirements.txt` com comentários

---

### 🚀 Próximos Passos

- ⏳ Implementar Flask-Limiter para rate limiting
- ⏳ Adicionar validação de variáveis obrigatórias no startup
- ⏳ Configurar CI/CD com testes automáticos
- ⏳ Documentar fluxo de auth em ADR-002
- ⏳ Implementar request logging estruturado (JSON)

---

### 🔗 Referências

- [OWASP A02:2021 – Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [OWASP A06:2021 – Security Misconfiguration](https://owasp.org/Top10/A06_2021-Security_Misconfiguration/)
- [Flask Configuration Best Practices](https://flask.palletsprojects.com/config/)
- [Session Cookie Security](https://flask.palletsprojects.com/en/2.3.x/security/#sessions)

---

**Versão**: 1.1.0  
**Data**: 2026-06-06  
**Status**: ✅ Implementado
