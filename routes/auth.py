"""
routes/auth.py
--------------
Rotas de autenticação e gerenciamento de usuários.
"""
from flask import render_template, request, redirect, url_for, session, flash
from forms import RegisterForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from services.auth_service import AuthService
from . import auth_bp


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Rota de registro de novo usuário."""
    form = RegisterForm()
    if form.validate_on_submit():
        result = AuthService.register_user(form.username.data, form.password.data)
        flash(result['message'])
        if result['success']:
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Rota de login."""
    form = LoginForm()
    if form.validate_on_submit():
        result = AuthService.authenticate_user(form.username.data, form.password.data)
        if result['success']:
            session['user_id'] = result['user'].id
            session.permanent = True
            return redirect(url_for('tasks.index'))
        flash(result['message'])
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """Rota de logout."""
    session.pop('user_id', None)
    flash('Logout realizado!')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Rota para alterar senha."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        result = AuthService.change_password(
            form.username.data,
            form.old_password.data,
            form.new_password.data
        )
        flash(result['message'])
        if result['success']:
            return redirect(url_for('auth.login'))
    return render_template('change_password.html', form=form)


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Rota para redefinir senha."""
    form = ResetPasswordForm()
    if form.validate_on_submit():
        result = AuthService.reset_password(form.username.data, form.new_password.data)
        flash(result['message'])
        if result['success']:
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)
