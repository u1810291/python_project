# coding=utf8
import math
import stripe
from werkzeug.datastructures import MultiDict
from . import forms
from app import db
from app.models import Invoice, Order, OrderItem
from sqlalchemy import asc, desc
from sqlalchemy.exc import DatabaseError
from flask_login import login_required, current_user
from flask import Blueprint, session, redirect, url_for, render_template, request, flash

module_cabinet = Blueprint('cabinet', __name__)


@module_cabinet.route('/', methods=('GET', ))
@login_required
def index():
    page = int(request.args.get('page', 1)) - 1
    on_page = 6 # todo: move to config
    offset = page * on_page
    limit = offset + on_page

    orders_query = Order.query.filter_by(user_id=current_user.id)
    orders = orders_query.order_by(desc(getattr(Order, 'updated_at'))).slice(offset, limit).all()

    pagination = {
        'page': page + 1,
        'total': int(math.ceil(orders_query.count() / on_page)),
        'on_page': on_page
    }

    return render_template(
        'modules/cabinet/index.html',
        orders=orders,
        pagination=pagination
    )


@module_cabinet.route('/import', methods=('GET',))
@login_required
def import_order():
    def clean():
        for key in ['user_info', 'consolidation_items', 'purchase_items']:
            if key in session:
                del session[key]

    user_info_data = session.get('user_info')
    consolidation_items_data = session.get('consolidation_items')
    purchase_items_data = session.get('purchase_items')

    if user_info_data is None:
        return redirect(url_for('.index'))

    if consolidation_items_data is None and purchase_items_data is None:
        return redirect(url_for('.index'))

    try:
        if consolidation_items_data is not None:
            order = Order(
                service=Order.SERVICE_CONSOLIDATION,
                status=Order.STATUS_STOCK_DELIVERY_WAITING,
                user_id=current_user.id,
                shipping_address=user_info_data['address']
            )

            for consolidation_item in consolidation_items_data:
                order_item = OrderItem(
                    url=consolidation_item['url'],
                    comment=consolidation_item['comment'],
                    quantity=consolidation_item['quantity'],
                    tracking_id=consolidation_item['tracking_id'],
                    price=consolidation_item['price'],
                )
                order.items.append(order_item)

            db.session.add(order)

        if purchase_items_data is not None:
            order = Order(
                service=Order.SERVICE_PURCHASE,
                status=Order.STATUS_PENDING,
                user_id=current_user.id,
                shipping_address=user_info_data['address']
            )

            for purchase_item in purchase_items_data:
                order_item = OrderItem(
                    url=purchase_item['url'],
                    comment=purchase_item['comment'],
                    quantity=purchase_item['quantity'],
                    size=purchase_item['size'],
                    color=purchase_item['color'],
                    discount=purchase_item['discount'],
                    price=purchase_item['price'],
                )
                order.items.append(order_item)

            db.session.add(order)

        db.session.commit()
        clean()
        return redirect(url_for('.index'))

    except DatabaseError as e:
        print(e)
        db.session.rollback()


@module_cabinet.route('/me', methods=('GET', 'POST'))
@login_required
def me():
    change_user_info_form = forms.ChangeUserInfo(MultiDict({
        'name': current_user.name,
        'phone': current_user.phone,
        'address': current_user.address
    }))
    change_password_form = forms.ChangePassword()

    if 'user_info_btn' in request.form:
        change_user_info_form = forms.ChangeUserInfo(MultiDict(request.form))
        if change_user_info_form.validate_on_submit():
            current_user.name = change_user_info_form.name.data
            current_user.phone = change_user_info_form.phone.data
            current_user.address = change_user_info_form.address.data
            db.session.add(current_user)
            db.session.commit()
            flash('Данные успешно сохранены!')

    if 'password_change_btn' in request.form:
        change_password_form = forms.ChangePassword(MultiDict(request.form))
        if change_password_form.validate_on_submit():
            current_user.password = change_password_form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Пароль успешно сменен!')

    return render_template(
        'modules/cabinet/me.html',
        change_user_info_form=change_user_info_form,
        change_password_form=change_password_form
    )


@module_cabinet.route('/checkout/<invoice_id>', methods=('GET', 'POST'))
@login_required
def checkout(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if invoice is None:
        return 'Not Found', 404

    if invoice.order.user_id != current_user.id:
        return 'Not Found', 404

    if invoice.is_paid:
        return 'Not Found', 404

    error_message = ''
    if request.method == 'POST':
        try:
            stripe_token = request.form['stripe_token']
            response = stripe.Charge.create(
                amount=int(invoice.total*100),
                currency="usd",
                source=stripe_token,
                description='Thank you for your purchase!',
                metadata={
                    'order_id': invoice.order.id,
                    'invoice_id': invoice.id,
                    'user_id': invoice.order.user.id,
                    'user_name': invoice.order.user.name
                }
            )

            invoice.is_paid = True
            invoice.stripe_id = response['id']
            if invoice.order.status == Order.STATUS_GOODS_PAYMENT_WAITING:
                invoice.order.status = Order.STATUS_STOCK_DELIVERY_WAITING

            if invoice.order.status == Order.STATUS_DELIVERY_PAYMENT_WAITING:
                invoice.order.status = Order.STATUS_CUSTOMER_DELIVERY_WAITING

            db.session.add(invoice)
            db.session.commit()

            print(response)
            print('ok')
            return redirect(url_for('cabinet.index'))

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            print(e)
            error_message = 'Неправильные данные карты'

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            print(e)
            error_message = 'Повторите попытку немного позже'

        except (stripe.error.InvalidRequestError, stripe.error.AuthenticationError, stripe.error.APIConnectionError, stripe.error.StripeError) as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            error_message = 'Что-то пошло не так'

    return render_template(
        'modules/cabinet/checkout.html',
        invoice=invoice,
        error_message=error_message
    )
