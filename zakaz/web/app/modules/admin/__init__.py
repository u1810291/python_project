# coding=utf8
from flask_admin import Admin
from .flask_admin_views import *


def init_admin_module(app):
    from app.models import User, Order, Page, Invoice
    from app import db

    admin = Admin(app, url=app.config['ADMIN_URL'], template_mode='bootstrap3')
    admin.add_view(UserModelView(User, db.session, name='Пользователи'))
    admin.add_view(OrderModelView(Order, db.session, name='Заказы'))
    admin.add_view(InvoiceModelView(Invoice, db.session, name='Инвойсы'))
    admin.add_view(PageModelView(Page, db.session, name='Страницы', endpoint='page-admin'))
