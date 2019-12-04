from . import forms
from app.helpers import is_json_ajax
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import MethodNotAllowed
from flask import Blueprint, render_template, request, jsonify, session, url_for
from flask_login import current_user

module_services = Blueprint('services', __name__)


@module_services.route('/consolidation', methods=('GET', 'POST'))
def consolidation():
    if request.method == 'POST':
        if not is_json_ajax():
            raise MethodNotAllowed()

        consolidation_form = forms.ConsolidationForm(request.json)
        error_response = []
        for item_form in consolidation_form.items:
            error_response_item = {}
            if not item_form.validate():
                for field in item_form.errors:
                    error_response_item[field] = '. '.join(item_form.errors[field])
            error_response.append(error_response_item)

        if any(item for item in error_response):
            return jsonify(error_response), 400

        consolidation_items = [item_form.data for item_form in consolidation_form.items]
        session['consolidation_items'] = consolidation_items
        return jsonify({}), 200

    else:
        consolidation_items = session.get('consolidation_items', [MultiDict()])
        consolidation_form = forms.ConsolidationForm({'items': consolidation_items})
        return render_template(
            'modules/services/consolidation.html',
            consolidation_form=consolidation_form
        )


@module_services.route('/purchase', methods=('GET','POST'))
def purchase():
    if request.method == 'POST':
        if not is_json_ajax():
            raise MethodNotAllowed()

        purchase_form = forms.PurchaseForm(request.json)
        error_response = []
        for item_form in purchase_form.items:
            error_response_item = {}
            if not item_form.validate():
                for field in item_form.errors:
                    error_response_item[field] = '. '.join(item_form.errors[field])
            error_response.append(error_response_item)

        if any(item for item in error_response):
            return jsonify(error_response), 400

        purchase_items = [item_form.data for item_form in purchase_form.items]
        session['purchase_items'] = purchase_items

        return jsonify({}), 200

    else:
        purchase_items = session.get('purchase_items', [MultiDict()])
        purchase_form = forms.PurchaseForm({'items': purchase_items})
        return render_template(
            'modules/services/purchase.html',
            purchase_form=purchase_form
        )


@module_services.route('/consolidation/user-info', methods=('GET', 'POST'), endpoint='consolidation_user_info')
@module_services.route('/purchase/user-info', methods=('GET', 'POST'), endpoint='purchase_user_info')
def user_info():
    if request.method == 'POST':
        if not is_json_ajax():
            raise MethodNotAllowed()

        if not current_user.is_authenticated:
            raise MethodNotAllowed()

        user_info_form = forms.UserInfoForm(MultiDict(request.json))
        if not user_info_form.validate():
            error_response = {}
            for field in user_info_form.errors:
                error_response[field] = '. '.join(user_info_form.errors[field])
            return jsonify(error_response), 400

        user_info_data = {
            'name': current_user.name,
            'email': current_user.email,
            'phone': current_user.phone,
            'address': user_info_form.address.data
        }
        session['user_info'] = user_info_data

        return jsonify({}), 200

    else:
        current_user_address = ''
        if current_user.is_authenticated:
            current_user_address = current_user.address

        user_info_form = forms.UserInfoForm(MultiDict({
            'address': current_user_address
        }))

        if request.url_rule.endpoint == 'services.consolidation_user_info':
            service_url = url_for('.consolidation')
        else:
            service_url = url_for('.purchase')

        return render_template(
            'modules/services/user_info.html',
            user_info_form=user_info_form,
            url_rule=request.url_rule,
            service_url=service_url
        )
