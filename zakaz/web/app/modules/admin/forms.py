# coding=utf8
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField, IntegerField, FloatField, FieldList, TextAreaField, FormField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import InputRequired, URL, NumberRange, Optional
from app.models import Order


class OrderItemForm(FlaskForm):
    url = URLField('URL', validators=[
        InputRequired('Обязательное поле'),
        URL('Неправильный адрес'),
    ])
    quantity = IntegerField('Количество', validators=[
        InputRequired('Обязательное поле'),
        NumberRange(min=0)
    ])
    weight = FloatField('Вес', validators=[
        Optional(),
        NumberRange(min=0)
    ])

    tracking_id = StringField('Tracking ID', validators=[])  # todo: conditional requiered
    price = FloatField('Цена товара на сайте', validators=[
        InputRequired("Это поле обязательно к заполнению"),
        NumberRange(min=0.01, message='Не правильное число')
    ])
    size = StringField('Размер', validators=[
        Optional()
    ])
    color = StringField('Цвет', validators=[
        Optional()
    ])
    discount = StringField('Промо-код', validators=[
        Optional()
    ])
    comment = TextAreaField('Комментарий', validators=[
        Optional()
    ])


class OrderInvoicePurchaseItem(FlaskForm):
    goods_price_total = FloatField('Общая стомость покупки товаров')


class OrderForm(FlaskForm):
    status = SelectField(
        'Статус',
        validators=[
            InputRequired("Обязательное поле"),
        ],
        choices=[(status, Order.get_status_label_by(status)) for status in Order.get_allowed_statuses()]
    )
    shipping_address = StringField('Адрес доставки', validators=[
        InputRequired('Обязательное поле')
    ])
    items = FieldList(FormField(OrderItemForm))


