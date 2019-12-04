# coding=utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, ValidationError, Length
from flask_login import current_user
from app.helpers import html_to_text


def is_password_valid(form, field):
    if form.old_password.data != current_user.password:
        raise ValidationError('Неправильный пароль')


class ChangeUserInfo(FlaskForm):
    name = StringField(
        'Имя и фамилия',
        validators=[
            InputRequired("Обязательное поле"),
            Length(max=256)
        ],
        filters=[
            html_to_text
        ]
    )
    address = StringField(
        'Адрес доставки',
        validators=[
            InputRequired("Обязательное поле"),
            Length(max=256)
        ],
        filters=[
            html_to_text
        ]
    )
    phone = StringField(
        'Контактный телефон',
        validators=[
            InputRequired("Обязательное поле"),
            Length(max=256)
        ],
        filters=[
            html_to_text
        ]
    )


class ChangePassword(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[
        InputRequired("Обязательное поле"),
        Length(max=256),
        is_password_valid
    ])
    new_password = PasswordField('Новый пароль', validators=[
        InputRequired("Обязательное поле"),
        EqualTo('new_password_confirm', message='Пароли не совпадают'),
        Length(min=6, max=256, message='Слишком короткий пароль. Минимум 6 симвлов.')
    ])
    new_password_confirm = PasswordField('Подтвердите пароль', validators=[
        InputRequired("Обязательное поле"),
    ])
