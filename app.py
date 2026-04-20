from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from forms import RegisterForm, LoginForm, ChangePasswordForm, TaskForm, ResetPasswordForm
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re



app = Flask(__name__)
app.config['SECRET_KEY'] = '#Ags@1984?'  # Troque por uma chave forte em produção
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


"""
app.py
---------
Aplicação principal Flask para gerenciamento de tarefas e subtarefas.
Inclui autenticação, cadastro, visualização, conclusão e exclusão de tarefas.

Boas práticas:
- Docstrings em módulos, classes e funções
- Comentários explicativos para trechos importantes
- Organização por seções: modelos, rotas, utilitários
"""

# --- MODELOS ---

class User(db.Model):
    """Modelo de usuário do sistema."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    """Modelo de tarefa principal, com campos de datas, status e relação com subtarefas."""
    id = db.Column(db.Integer, primary_key=True)
    id_of = db.Column(db.String(50), nullable=False)
    task = db.Column(db.String(10), nullable=False)
    id_num = db.Column(db.Integer, nullable=False)
    segment = db.Column(db.String(10), nullable=False)
    area = db.Column(db.String(10), nullable=False)
    objective = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    completion_date = db.Column(db.String(20), nullable=True)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    atraso_dias = db.Column(db.Integer, nullable=True, default=0)

    def calcular_atraso(self):
        """
        Calcula o atraso em dias entre a data de conclusão e o prazo da tarefa.
        Aceita formatos de data flexíveis.
        """
        if self.completion_date and self.due_date:
            formats = ["%Y-%m-%d", "%d-%m-%Y"]
            d_due = d_comp = None
            
            for fmt in formats:
                try:
                    if not d_due: d_due = datetime.strptime(self.due_date.strip(), fmt)
                except ValueError: continue
            
            for fmt in formats:
                try:
                    if not d_comp: d_comp = datetime.strptime(self.completion_date.strip(), fmt)
                except ValueError: continue

            if d_due and d_comp:
                diff = (d_comp - d_due).days
                self.atraso_dias = diff if diff > 0 else 0

class Subtask(db.Model):
    """Modelo de subtarefa vinculada a uma tarefa principal."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completion_date = db.Column(db.String(20), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('subtasks', lazy=True))

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe!')
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado! Faça login.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        flash('Usuário ou senha inválidos!')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        old_pw = form.old_password.data
        new_pw = form.new_password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, old_pw):
            user.password = generate_password_hash(new_pw)
            db.session.commit()
            flash('Senha alterada! Faça login.')
            return redirect(url_for('login'))
        else:
            flash('Usuário ou senha antiga incorretos!')
    return render_template('change_password.html', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        new_pw = form.new_password.data
        user = User.query.filter_by(username=username).first()
        if user:
            user.password = generate_password_hash(new_pw)
            db.session.commit()
            flash('Senha redefinida! Faça login.')
            return redirect(url_for('login'))
        else:
            flash('Usuário não encontrado!')
    return render_template('reset_password.html', form=form)

# --- ROTAS DE TAREFAS ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal: formulário de criação de tarefas e subtarefas.
    Se método POST e formulário válido, salva tarefa e subtarefas no banco.
    """
    if 'user_id' not in session: return redirect(url_for('login'))
    form = TaskForm()
    if form.validate_on_submit():
        prefix = form.id_of.data.upper()
        # Busca IDs existentes com mesmo prefixo
        existing = Task.query.filter(Task.id_of.like(f'{prefix}%')).all()
        nums = [int(t.id_of[3:]) for t in existing if t.id_of[:3].upper() == prefix and t.id_of[3:].isdigit()]
        next_num = 1
        if nums:
            next_num = max(nums) + 1
        id_of_final = f"{prefix}{next_num:04d}"
        task_type = form.task.data
        last_t = Task.query.filter_by(task=task_type).order_by(Task.id_num.desc()).first()
        task_id_num = 1 if not last_t else last_t.id_num + 1
        new_task = Task(
            id_of=id_of_final,
            task=task_type,
            id_num=task_id_num,
            segment=form.segment.data,
            area=form.area.data,
            objective=form.objective.data,
            description=form.description.data,
            start_date=form.start_date.data.strftime('%Y-%m-%d'),
            due_date=form.due_date.data.strftime('%Y-%m-%d'),
            completion_date=form.completion_date.data.strftime('%Y-%m-%d') if form.completion_date.data else None,
            priority=form.priority.data,
            status=form.status.data,
            user_id=session['user_id']
        )
        if new_task.completion_date:
            new_task.calcular_atraso()
        db.session.add(new_task)
        db.session.commit()
        for i in range(1, 4):
            sub_name = getattr(form, f'subtask{i}').data
            if sub_name:
                db.session.add(Subtask(name=sub_name, task_id=new_task.id))
        db.session.commit()
        return redirect(url_for('view_tasks'))
    else:
        if form.errors:
            print('ERROS DE VALIDAÇÃO:', form.errors)
    return render_template('index.html', form=form)

@app.route('/view')
def view_tasks():
    """
    Rota de visualização de tarefas e subtarefas cadastradas (todas as tarefas de todos os usuários).
    """
    if 'user_id' not in session: return redirect(url_for('login'))
    tasks = Task.query.order_by(Task.user_id, Task.id_of, Task.id_num).all()
    return render_template('view.html', tasks=tasks)

@app.route('/done/<int:task_id>')
def done_task(task_id):
    """
    Marca uma tarefa como concluída, preenchendo a data de conclusão.
    """
    task = Task.query.get_or_404(task_id)
    if task.user_id != session.get('user_id'): return redirect(url_for('view_tasks'))
    
    if not task.completion_date:
        task.completion_date = datetime.today().strftime('%Y-%m-%d')
        task.status = 'completed'
        task.calcular_atraso()
        db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """
    Exclui uma tarefa e suas subtarefas do banco de dados.
    """
    task = Task.query.get_or_404(task_id)
    if task.user_id == session.get('user_id'):
        Subtask.query.filter_by(task_id=task.id).delete()
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('view_tasks'))

# --- ROTAS DE SUBTAREFAS ---

@app.route('/subtask/done/<int:subtask_id>')
def done_subtask(subtask_id):
    """
    Marca uma subtarefa como concluída.
    """
    sub = Subtask.query.get_or_404(subtask_id)
    if not sub.completion_date:
        sub.completion_date = datetime.today().strftime('%d-%m-%Y')
        db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/subtask/delete/<int:subtask_id>')
def delete_subtask(subtask_id):
    """
    Exclui uma subtarefa do banco de dados.
    """
    sub = Subtask.query.get_or_404(subtask_id)
    db.session.delete(sub)
    db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)