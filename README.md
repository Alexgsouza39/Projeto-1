# Projeto de Gerenciamento de Tarefas

Este projeto é uma aplicação web desenvolvida com Flask para cadastro, visualização, conclusão e exclusão de tarefas e subtarefas. Possui autenticação de usuários, proteção CSRF, validação de formulários, interface responsiva e testes automatizados.

## Funcionalidades
- Cadastro e login de usuários
- Criação de tarefas com campos detalhados
- Inclusão de até 3 subtarefas por tarefa
- Marcação de tarefas e subtarefas como concluídas
- Exclusão de tarefas e subtarefas
- Filtro de pesquisa em tempo real (tasks e subtasks)
- Exibição de atrasos em dias
- Interface responsiva para desktop e mobile
- Proteção CSRF e validação WTForms
- Testes automatizados

## Instalação
1. Clone o repositório
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python app.py
   ```

## Estrutura de Pastas
- `app.py` — Backend Flask, rotas, modelos
- `forms.py` — Formulários WTForms
- `templates/` — Templates HTML (Jinja2)
- `static/` — Arquivos estáticos (CSS, favicon)
- `requirements.txt` — Dependências
- `test_site.py` — Testes automatizados

## Rotas da Aplicação

### Autenticação
- `GET /register` — Exibe formulário de cadastro
- `POST /register` — Processa cadastro de novo usuário
- `GET /login` — Exibe formulário de login
- `POST /login` — Processa login
- `GET /logout` — Faz logout do usuário
- `GET, POST /change_password` — Troca de senha

### Tarefas
- `GET, POST /` — Página principal, formulário de criação de tarefas e subtarefas
- `GET /view` — Visualização de todas as tarefas e subtarefas do usuário logado
- `GET /done/<int:task_id>` — Marca tarefa como concluída
- `GET /delete/<int:task_id>` — Exclui tarefa e suas subtarefas

### Subtarefas
- `GET /subtask/done/<int:subtask_id>` — Marca subtarefa como concluída
- `GET /subtask/delete/<int:subtask_id>` — Exclui subtarefa

### Outros
- `GET /favicon.ico` — Favicon do site

## Observações
- O campo "completion_date" é opcional ao criar tarefas. Pode ser preenchido depois ao marcar como concluída.
- O filtro de pesquisa exibe sempre a tarefa e todas as subtarefas relacionadas quando houver correspondência.
- O sistema utiliza SQLite por padrão.

## Testes
Execute os testes automatizados com:
```bash
python test_site.py
```

## Licença

Este projeto está licenciado sob a Licença MIT.

Copyright (c) 2024 Alex Guariroba de Souza.

A permissão é concedida, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados, para lidar com o software sem restrição, incluindo, sem limitação, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software, sujeito às seguintes condições:

O aviso de copyright acima e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do software.

O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO. EM NENHUM CASO OS AUTORES OU DETENTORES DE DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER REIVINDICAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM UMA AÇÃO DE CONTRATO, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, FORA DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.
