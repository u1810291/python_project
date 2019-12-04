# coding=utf8
from flask import request, redirect
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.helpers import get_mdict_item_or_list
from werkzeug.datastructures import MultiDict
from .forms import OrderForm
from flask_login import current_user


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class UserModelView(CustomModelView):
    can_create = False
    can_edit = True
    can_delete = False
    create_modal = False
    edit_modal = True

    column_list = ('name', 'email', 'address', 'phone')
    column_labels = dict(name='Имя', email='E-mail', address='Адрес по-умолчанию', phone='Контактный телефон')
    column_sortable_list = ('name', 'email')
    column_searchable_list = ('name', 'email', 'address', 'phone')
    column_filters = ('name', 'email', 'address', 'phone')

    # form_columns = (,)
    form_excluded_columns = ['password', 'created_at', 'updated_at', 'orders', 'email', 'is_admin']


class OrderModelView(CustomModelView):
    can_create = False
    can_edit = True
    can_delete = True

    # todo: кол-во товаров,
    column_list = ('id', 'status', 'service', 'items_count', 'user', 'shipping_address', 'created_at', 'updated_at')
    column_labels = dict(id='№', status='Статус', service='Услуга', items_count='Количество товаров', user='Заказчик',
                         shipping_address='Адрес доставки', created_at='Дата добавления', updated_at='Дата обновления')
    column_sortable_list = ('status', 'service', 'created_at', 'updated_at')
    column_searchable_list = ('user.name',)
    column_filters = ('id', 'status', 'service', 'user.name', 'user.email', 'user.phone', 'user.address')
    column_default_sort = ('updated_at', True)
    column_formatters = dict(
        user=lambda v, c, m, p: m.user.name,
        status=lambda v, c, m, p: m.status_label,
        service=lambda v, c, m, p: m.service_label,
        items_count=lambda v, c, m, p: len(m.items),
        created_at=lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M'),
        updated_at=lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M')
    )

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        from app.models import Order, Invoice
        from app import db

        return_url = self.get_url('.index_view')
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        order = Order.query.get(id)
        if order is None:
            return redirect(return_url)

        order_form = OrderForm(obj=order)
        if request.method == 'POST':
            if 'action_consolidation_invoice_submit' in request.form:
                delivery_total = float(request.form['delivery_total'])
                new_invoice = order.invoice_consolidation
                if new_invoice is None:
                    new_invoice = Invoice(order_id=order.id, type=Invoice.TYPE_CONSOLIDATION)
                new_invoice.delivery_total = delivery_total
                db.session.add(new_invoice)
                db.session.commit()

            elif 'action_purchase_invoice_submit' in request.form:
                goods_price_total = float(request.form['goods_price_total'])
                new_invoice = order.invoice_purchase
                if new_invoice is None:
                    new_invoice = Invoice(order_id=order.id, type=Invoice.TYPE_PURCHASE)
                new_invoice.goods_price_total = goods_price_total
                db.session.add(new_invoice)
                db.session.commit()

            elif 'action_remove_invoice' in request.form:
                invoice_id = request.form['invoice_id']
                invoice_query = Invoice.query.filter_by(id=invoice_id)
                invoice = invoice_query.first()
                if invoice and not invoice.is_paid:
                    invoice_query.delete()
                    db.session.commit()

            else:
                order_form = OrderForm(request.form)
                if order_form.validate_on_submit():
                    order.status = order_form.status.data
                    order.shipping_address = order_form.shipping_address.data
                    for i, item in enumerate(order_form.items):
                        order.items[i].url = item.url.data
                        order.items[i].quantity = item.quantity.data
                        order.items[i].weight = item.weight.data
                        order.items[i].tracking_id = item.tracking_id.data
                        order.items[i].size = item.size.data
                        order.items[i].color = item.color.data
                        order.items[i].discount = item.discount.data
                        order.items[i].comment = item.comment.data
                        order.items[i].price = item.price.data

                    db.session.add(order)
                    db.session.commit()

            return redirect(request.full_path)

        return self.render(
            'modules/admin/order/edit.html',
            order=order,
            order_form=order_form,
            return_url=return_url
        )


class PageModelView(CustomModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ('slug', 'title')
    column_labels = dict(slug='Адрес', title='Заголовок')
    #
    form_excluded_columns = ['created_at', 'updated_at']
    form_args = dict(
        content=dict(
            label='Содержание',
        )
    )


class InvoiceModelView(CustomModelView):
    can_create = False
    can_edit = False
    can_delete = False

    column_list = ('type', 'is_paid', 'order.id', 'order.user.name', 'goods_price_total', 'simsim_commission', 'delivery_total', 'total', 'created_at', 'updated_at')
    column_labels = {'type': 'Тип', 'is_paid': 'Оплачен?', 'order.id': 'ID заказа', 'order.user.name': 'Заказчик', 'goods_price_total': 'Цена за покупку товаров',
                     'simsim_commission': 'Комиссия Sim Sim', 'delivery_total': 'Цена за доставку', 'total': 'Итого',
                     'created_at': 'Создан', 'updated_at': 'Обновлен'}
    column_sortable_list = ('goods_price_total', 'delivery_total', 'created_at', 'updated_at')
    column_searchable_list = ('order.user.name',)
    column_filters = ('type', 'order.id', 'is_paid')
    column_default_sort = ('updated_at', True)
    column_formatters = {
        'created_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M')
    }
