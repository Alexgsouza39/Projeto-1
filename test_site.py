import unittest
from app import app, db, User, Task
from flask import url_for
import datetime

class SiteTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def register(self, username, password):
        return self.app.post('/register', data=dict(
            username=username,
            password=password,
            submit='Register'
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password,
            submit='Login'
        ), follow_redirects=True)

    def test_register_and_login(self):
        rv = self.register('user1', 'senha123')
        self.assertIn(b'Cadastro realizado', rv.data, msg='Erro ao registrar usuário')
        rv = self.login('user1', 'senha123')
        # Alterado de 'Tasks' para 'Save Task' (que existe no seu botão) ou 'tarefas'
        self.assertIn(b'Save Task', rv.data, msg='Erro ao fazer login: Texto esperado não encontrado')

    def test_create_task(self):
        self.register('user2', 'senha123')
        self.login('user2', 'senha123')
        rv = self.app.post('/', data={
            'id_of': 'ORD',  # Corrigido para 3 caracteres
            'task': 'T1',
            'segment': 'S1',
            'area': 'A1',
            'objective': 'O1',
            'description': 'desc',
            'start_date': '2026-01-01',
            'due_date': '2026-01-02',
            # Não enviar completion_date se vazio
            'priority': 'low',
            'status': 'in course',  # Corrigido para valor aceito
            'subtask1': '',
            'subtask2': '',
            'subtask3': '',
            'submit': 'Save Task'
        }, follow_redirects=True)
        # Verifique se a sua view.html realmente contém "My Tasks". 
        # Se o sistema for em português, talvez deva ser 'tarefas' ou 'Status'.
        self.assertIn(b'Order', rv.data, msg='Erro ao criar tarefa: Redirecionamento para visualização falhou')

    def test_view_tasks_requires_login(self):
        rv = self.app.get('/view', follow_redirects=True)
        self.assertIn(b'Login', rv.data, msg='Acesso a /view sem login não redireciona')

if __name__ == '__main__':
    unittest.main()
