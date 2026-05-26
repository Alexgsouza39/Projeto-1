"""
models/task.py
--------------
Modelo de tarefa principal com campos de datas, status e relação com subtarefas.
"""
from datetime import datetime
from . import db


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
    subtasks = db.relationship('Subtask', backref='task_rel', lazy=True, cascade='all, delete-orphan')

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
                    if not d_due: 
                        d_due = datetime.strptime(self.due_date.strip(), fmt)
                except ValueError: 
                    continue
            
            for fmt in formats:
                try:
                    if not d_comp: 
                        d_comp = datetime.strptime(self.completion_date.strip(), fmt)
                except ValueError: 
                    continue

            if d_due and d_comp:
                diff = (d_comp - d_due).days
                self.atraso_dias = diff if diff > 0 else 0
