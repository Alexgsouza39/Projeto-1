"""
routes/tasks.py
---------------
Rotas de gerenciamento de tarefas e subtarefas.
"""
from flask import render_template, request, redirect, url_for, session, flash
from functools import wraps
from forms import TaskForm
from services.task_service import TaskService
from . import tasks_bp


def login_required(f):
    """Decorador para proteger rotas que requerem login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado!')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@tasks_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Rota principal: formulário de criação de tarefas e subtarefas.
    Se método POST e formulário válido, salva tarefa e subtarefas no banco.
    """
    form = TaskForm()
    if form.validate_on_submit():
        task_data = {
            'id_of': form.id_of.data,
            'task': form.task.data,
            'segment': form.segment.data,
            'area': form.area.data,
            'objective': form.objective.data,
            'description': form.description.data,
            'start_date': form.start_date.data.strftime('%Y-%m-%d'),
            'due_date': form.due_date.data.strftime('%Y-%m-%d'),
            'completion_date': form.completion_date.data.strftime('%Y-%m-%d') if form.completion_date.data else None,
            'priority': form.priority.data,
            'status': form.status.data,
            'subtask1': form.subtask1.data,
            'subtask2': form.subtask2.data,
            'subtask3': form.subtask3.data,
        }
        result = TaskService.create_task(task_data, session['user_id'])
        flash(result['message'])
        if result['success']:
            return redirect(url_for('tasks.view_tasks'))
    
    return render_template('index.html', form=form)


@tasks_bp.route('/view')
@login_required
def view_tasks():
    """
    Rota de visualização de tarefas e subtarefas cadastradas.
    Mostra todas as tarefas de todos os usuários.
    """
    tasks = TaskService.get_all_tasks()
    return render_template('view.html', tasks=tasks)


@tasks_bp.route('/done/<int:task_id>')
@login_required
def done_task(task_id):
    """Marca uma tarefa como concluída."""
    result = TaskService.mark_task_done(task_id, session['user_id'])
    flash(result['message'])
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    """Exclui uma tarefa e suas subtarefas do banco de dados."""
    result = TaskService.delete_task(task_id, session['user_id'])
    flash(result['message'])
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/subtask/done/<int:subtask_id>')
@login_required
def done_subtask(subtask_id):
    """Marca uma subtarefa como concluída."""
    result = TaskService.mark_subtask_done(subtask_id)
    flash(result['message'])
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/subtask/delete/<int:subtask_id>')
@login_required
def delete_subtask(subtask_id):
    """Exclui uma subtarefa do banco de dados."""
    result = TaskService.delete_subtask(subtask_id)
    flash(result['message'])
    return redirect(url_for('tasks.view_tasks'))
