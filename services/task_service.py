"""
services/task_service.py
------------------------
Serviço de gerenciamento de tarefas e subtarefas.
"""
from datetime import datetime
from models import db
from models.task import Task
from models.subtask import Subtask


class TaskService:
    """Serviço para gerenciamento de tarefas."""
    
    @staticmethod
    def create_task(task_data, user_id):
        """
        Cria uma nova tarefa com subtarefas.
        
        Args:
            task_data: dict com dados da tarefa
            user_id: ID do usuário proprietário
            
        Returns:
            dict: {'success': bool, 'message': str, 'task': Task or None}
        """
        try:
            # Gera ID único
            prefix = task_data.get('id_of', 'TSK').upper()
            existing = Task.query.filter(Task.id_of.like(f'{prefix}%')).all()
            nums = [int(t.id_of[3:]) for t in existing 
                    if t.id_of[:3].upper() == prefix and t.id_of[3:].isdigit()]
            next_num = 1 if not nums else max(nums) + 1
            id_of_final = f"{prefix}{next_num:04d}"
            
            # Gera número sequencial de tarefa
            task_type = task_data.get('task', 'DEFAULT')
            last_t = Task.query.filter_by(task=task_type).order_by(Task.id_num.desc()).first()
            task_id_num = 1 if not last_t else last_t.id_num + 1
            
            new_task = Task(
                id_of=id_of_final,
                task=task_type,
                id_num=task_id_num,
                segment=task_data.get('segment', ''),
                area=task_data.get('area', ''),
                objective=task_data.get('objective', ''),
                description=task_data.get('description', ''),
                start_date=task_data.get('start_date'),
                due_date=task_data.get('due_date'),
                completion_date=task_data.get('completion_date'),
                priority=task_data.get('priority', 'normal'),
                status=task_data.get('status', 'pending'),
                user_id=user_id
            )
            
            if new_task.completion_date:
                new_task.calcular_atraso()
            
            db.session.add(new_task)
            db.session.commit()
            
            # Adiciona subtarefas
            for i in range(1, 4):
                subtask_name = task_data.get(f'subtask{i}')
                if subtask_name:
                    db.session.add(Subtask(name=subtask_name, task_id=new_task.id))
            db.session.commit()
            
            return {'success': True, 'message': 'Tarefa criada com sucesso!', 'task': new_task}
        except Exception as e:
            return {'success': False, 'message': f'Erro ao criar tarefa: {str(e)}', 'task': None}
    
    @staticmethod
    def get_all_tasks():
        """Retorna todas as tarefas ordenadas."""
        return Task.query.order_by(Task.user_id, Task.id_of, Task.id_num).all()
    
    @staticmethod
    def get_user_tasks(user_id):
        """Retorna tarefas de um usuário específico."""
        return Task.query.filter_by(user_id=user_id).order_by(Task.id_of, Task.id_num).all()
    
    @staticmethod
    def mark_task_done(task_id, user_id):
        """
        Marca uma tarefa como concluída.
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        task = Task.query.get(task_id)
        if not task:
            return {'success': False, 'message': 'Tarefa não encontrada!'}
        
        if task.user_id != user_id:
            return {'success': False, 'message': 'Acesso negado!'}
        
        if task.completion_date:
            return {'success': False, 'message': 'Tarefa já foi concluída!'}
        
        task.completion_date = datetime.today().strftime('%Y-%m-%d')
        task.status = 'completed'
        task.calcular_atraso()
        db.session.commit()
        
        return {'success': True, 'message': 'Tarefa marcada como concluída!'}
    
    @staticmethod
    def delete_task(task_id, user_id):
        """
        Exclui uma tarefa e suas subtarefas.
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        task = Task.query.get(task_id)
        if not task:
            return {'success': False, 'message': 'Tarefa não encontrada!'}
        
        if task.user_id != user_id:
            return {'success': False, 'message': 'Acesso negado!'}
        
        try:
            Subtask.query.filter_by(task_id=task.id).delete()
            db.session.delete(task)
            db.session.commit()
            return {'success': True, 'message': 'Tarefa deletada com sucesso!'}
        except Exception as e:
            return {'success': False, 'message': f'Erro ao deletar tarefa: {str(e)}'}
    
    @staticmethod
    def mark_subtask_done(subtask_id):
        """
        Marca uma subtarefa como concluída.
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        sub = Subtask.query.get(subtask_id)
        if not sub:
            return {'success': False, 'message': 'Subtarefa não encontrada!'}
        
        if sub.completion_date:
            return {'success': False, 'message': 'Subtarefa já foi concluída!'}
        
        sub.completion_date = datetime.today().strftime('%d-%m-%Y')
        db.session.commit()
        
        return {'success': True, 'message': 'Subtarefa marcada como concluída!'}
    
    @staticmethod
    def delete_subtask(subtask_id):
        """
        Exclui uma subtarefa.
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        sub = Subtask.query.get(subtask_id)
        if not sub:
            return {'success': False, 'message': 'Subtarefa não encontrada!'}
        
        try:
            db.session.delete(sub)
            db.session.commit()
            return {'success': True, 'message': 'Subtarefa deletada com sucesso!'}
        except Exception as e:
            return {'success': False, 'message': f'Erro ao deletar subtarefa: {str(e)}'}
