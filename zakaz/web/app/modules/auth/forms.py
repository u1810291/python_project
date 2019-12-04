# coding=utf8
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired, EqualTo, DataRequired, ValidationError, Length
from app.models import User
from app.helpers import html_to_text

def is_not_exists_user(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    if user is None:
        raise ValidationError('Неправильный логин или пароль')


def is_exists_user(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None:
        raise ValidationError('Такой email уже зарегистрирован в системе')


class SignIn(FlaskForm):
    email = EmailField('E-mail', validators=[
        InputRequired("Пожалуйста, укажите ваш e-mail адрес"),
        Email("Неправильный email адрес"),
        Length(max=256),
        is_not_exists_user
    ])
    password = PasswordField('Пароль', validators=[
        InputRequired("Пожалуйста, укажите пароль"),
        Length(max=256),
    ])


class SignUp(FlaskForm):
    name = StringField(
        'Имя и фамилия',
        validators=[
            InputRequired("Пожалуйста, укажите ваше имя и фамилию"),
            Length(max=256),
        ],
        filters=[
            html_to_text
    ])
    address = StringField(
        'Адрес доставки',
        validators=[
            InputRequired("Пожалуйста, укажите куда доставить вашу посылку"),
            Length(max=256),
        ],
        filters=[
            html_to_text
        ]
    )
    phone = StringField(
        'Контактный телефон',
        validators=[
            InputRequired("Пожалуйста, оставьте контатный телефон"),
            Length(max=256),
        ],
        filters=[
            html_to_text
        ]
    )
    email = EmailField('E-mail', validators=[
        InputRequired("Пожалуйста, укажите ваш email"),
        Email("Неправильный email"),
        Length(max=256),
        is_exists_user
    ])
    password = PasswordField('Введите пароль', validators=[
        InputRequired("Пожалуйста, введите Ваш пароль"),
        EqualTo('password_confirm', message='Пароли не совпадают'),
        Length(min=6, max=256,message='Слишком короткий пароль. Минимум 6 симвлов.')
    ])
    password_confirm = PasswordField('Повторите пароль', validators=[
        InputRequired("Нужно повторить пароль"),
    ])
    recaptcha = RecaptchaField()


class RestoreInit(FlaskForm):
    email = EmailField('E-mail', validators=[
        InputRequired("Пожалуйста, укажите ваш email"),
        Email("Неправильный email"),
        Length(max=256),
    ])


class Restore(FlaskForm):
    restore_token = StringField()
    password = PasswordField('Новый пароль', validators=[
        InputRequired("Пожалуйста, укажите новый пароль"),
        EqualTo('password_confirm', message='Пароли не совпадают'),
        Length(min=6, max=256),
    ])
    password_confirm = PasswordField('Повторите новый пароль', validators=[
        InputRequired("Пороль надо повторить"),
    ])
