from flask import request
from werkzeug.datastructures import MultiDict


def detect_return_route():
    return request.args.get('return_to', '/')


def build_signup_form_data():
    signup_form_data = {
        'name': request.args.get('name'),
        'email': request.args.get('email'),
        'address': request.args.get('address'),
        'phone': request.args.get('phone'),
    }
    signup_form_data.update(request.form)
    return MultiDict(signup_form_data)
