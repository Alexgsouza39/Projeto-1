"""
services/auth_service.py
------------------------
Serviço de autenticação e gerenciamento de usuários.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User


class AuthService:
    """Serviço de autenticação."""
    
    @staticmethod
    def register_user(username, password):
        """
        Registra um novo usuário no sistema.
        
        Returns:
            dict: {'success': bool, 'message': str, 'user': User or None}
        """
        if User.query.filter_by(username=username).first():
            return {'success': False, 'message': 'Usuário já existe!', 'user': None}
        
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return {'success': True, 'message': 'Cadastro realizado com sucesso!', 'user': new_user}
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Autentica um usuário.
        
        Returns:
            dict: {'success': bool, 'message': str, 'user': User or None}
        """
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return {'success': True, 'message': 'Autenticação bem-sucedida!', 'user': user}
        return {'success': False, 'message': 'Usuário ou senha inválidos!', 'user': None}
    
    @staticmethod
    def change_password(username, old_password, new_password):
        """
        Altera a senha de um usuário.
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'success': False, 'message': 'Usuário não encontrado!'}
        
        if not check_password_hash(user.password, old_password):
            return {'success': False, 'message': 'Senha antiga incorreta!'}
        
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return {'success': True, 'message': 'Senha alterada com sucesso!'}
    
    @staticmethod
    def reset_password(username, new_password):
        """
        Redefine a senha de um usuário (sem verificar senha antiga).
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'success': False, 'message': 'Usuário não encontrado!'}
        
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return {'success': True, 'message': 'Senha redefinida com sucesso!'}
