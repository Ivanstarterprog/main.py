from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, FileField
from wtforms.fields import EmailField, SelectField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileAllowed


class RegisterForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    patronymic = StringField('Отчество пользователя')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_confirm = PasswordField('Повторите пароль',
                                   validators=[DataRequired(),
                                               EqualTo('password',
                                                       message='Пароли должны совпадать!')])
    avatar = FileField("Фотография", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    group = SelectField('Группа')
    role = SelectField('Роль', choices=["Студент", "Учитель", "Администратор"])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Войти')