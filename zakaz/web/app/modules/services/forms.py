# coding=utf8
from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict
from wtforms import StringField, TextAreaField, BooleanField, FloatField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, URL, NumberRange, Length
from app.helpers import html_to_text


class ConsolidationItem(FlaskForm):
    url = StringField('Ссылка на товар*', validators=[
        InputRequired("Это поле обязательно к заполнению"),
        URL(message="Неправильная ссылка"),
        Length(max=2048),
    ])
    tracking_id = StringField(
        'Tracking ID*',
        validators=[
            InputRequired("Это поле обязательно к заполнению"),
            Length(max=256),
        ],
        filters=[
            html_to_text
        ]
    )
    quantity = IntegerField('Количество*', validators=[
        InputRequired("Это поле обязательно к заполнению"),
        NumberRange(min=1, max=1000, message="Количество должно быть от %(min)s до %(max)s")
    ])
    price = FloatField('Цена товара на сайте*', validators=[
        InputRequired("Это поле обязательно к заполнению"),
        NumberRange(min=0.01, message='Не правильное число')
    ])
    comment = TextAreaField(
        'Комментарий',
        validators=[
            Length(max=2048),
        ],
        filters=[
            html_to_text
        ]
    )


class ConsolidationForm(object):
    # todo: find the best way to doing this
    def __init__(self, data):
        self.items = []
        for item_data in data['items']:
            self.items.append(ConsolidationItem(MultiDict(item_data)))

        self._normalize_items()

    def validate(self):
        return all(item.validate() for item in self.items)

    def _normalize_items(self):
        for consolidation_item in self.items:
            consolidation_item.url.name = 'items[][url]'
            consolidation_item.tracking_id.name = 'items[][tracking_id]'
            consolidation_item.quantity.name = 'items[][quantity]'
            consolidation_item.comment.name = 'items[][comment]'
            consolidation_item.price.name = 'items[][price]'


class PurchaseItem(FlaskForm):
    url = StringField('Ссылка на товар*', validators=[
        InputRequired("Это поле обязательно к заполнению"),
        URL(message="Неправильная ссылка"),
        Length(max=2048),
    ])
    quantity = IntegerField('Количество*', validators=[
        InputRequired("Это поле обязательно к заполнению"),
        NumberRange(min=1, max=1000, message="Количество должно быть от %(min)s до %(max)s")
    ])
    price = FloatField('Цена товара на сайте*', validators=[
        InputRequired("Это поле обязательно к заполнению"),
        NumberRange(min=0.01, message='Не правильное число')
    ])
    size = StringField(
        'Размер',
        validators=[
            Length(max=256),
        ],
        filters=[
            html_to_text
        ]
    )
    color = StringField(
        'Цвет',
        validators=[
            Length(max=256),
        ],
        filters=[
            html_to_text
        ]
    )
    discount = StringField(
        'Промо код',
        validators=[
            Length(max=256),
        ],
        filters=[
            html_to_text
        ]
    )
    comment = TextAreaField(
        'Комментарий',
        validators=[
            Length(max=2048),
        ],
        filters=[
            html_to_text
        ]
    )


class PurchaseForm(object):
    # todo: find the best way to doing this
    def __init__(self, data):
        self.items = []
        for item_data in data['items']:
            self.items.append(PurchaseItem(MultiDict(item_data)))

        self._normalize_items()

    def validate(self):
        return all(item.validate() for item in self.items)

    def _normalize_items(self):
        for purchase_item in self.items:
            purchase_item.url.name = 'items[][url]'
            purchase_item.quantity.name = 'items[][quantity]'
            purchase_item.size.name = 'items[][size]'
            purchase_item.color.name = 'items[][color]'
            purchase_item.comment.name = 'items[][comment]'
            purchase_item.price.name = 'items[][price]'


class UserInfoForm(FlaskForm):
    address = StringField(
        'Адрес доставки',
        validators=[
            InputRequired("Это поле обязательно к заполнению")
        ],
        filters=[
            html_to_text
        ]
    )
