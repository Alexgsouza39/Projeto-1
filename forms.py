from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
import re

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    old_password = PasswordField('Senha atual', validators=[DataRequired()])
    new_password = PasswordField('Nova senha', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Alterar Senha')

class ResetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('Nova senha', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Redefinir Senha')

class TaskForm(FlaskForm):
    def validate_id_of(self, field):
        value = field.data
        # Validação: apenas 3 letras
        if not re.match(r'^[A-Za-z]{3}$', value):
            raise ValidationError('ID deve conter exatamente 3 letras.')
    id_of = StringField('Order', validators=[DataRequired(), Length(min=3, max=3)])
    task = SelectField('Task', choices=[('T1','T1'),('T2','T2'),('T3','T3')], validators=[DataRequired()])
    segment = SelectField('Segment', choices=[('S1','S1'),('S2','S2'),('S3','S3')], validators=[DataRequired()])
    area = SelectField('Area', choices=[('A1','A1'),('A2','A2'),('A3','A3')], validators=[DataRequired()])
    objective = SelectField('Objective', choices=[('O1','O1'),('O2','O2'),('O3','O3')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    completion_date = DateField('Completion Date', format='%Y-%m-%d', validators=[Optional()], default=None)
    priority = SelectField('Priority', choices=[('low','Low'),('medium','Medium'),('high','High')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('in course','In Course'),('completed','Completed')], validators=[DataRequired()])
    subtask1 = TextAreaField('Subtask1')
    subtask2 = TextAreaField('Subtask2')
    subtask3 = TextAreaField('Subtask3')
    submit = SubmitField('Save Task')
