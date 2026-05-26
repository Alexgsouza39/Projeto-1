"""
services/user_service.py
------------------------
Serviço de gerenciamento de usuários.
"""
from models import db
from models.user import User


class UserService:
    """Serviço para gerenciamento de usuários."""
    
    @staticmethod
    def get_user_by_id(user_id):
        """Retorna um usuário pelo ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Retorna um usuário pelo nome de usuário."""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_all_users():
        """Retorna todos os usuários."""
        return User.query.all()
    
    @staticmethod
    def delete_user(user_id):
        """
        Deleta um usuário e suas tarefas.
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'message': 'Usuário não encontrado!'}
        
        try:
            db.session.delete(user)
            db.session.commit()
            return {'success': True, 'message': 'Usuário deletado com sucesso!'}
        except Exception as e:
            return {'success': False, 'message': f'Erro ao deletar usuário: {str(e)}'}
