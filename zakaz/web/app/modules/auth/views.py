# coding=utf8
from . import forms, helpers
from app.helpers import is_json_ajax
from app.models import User
from app import db
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import MethodNotAllowed, NotFound
from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

module_auth = Blueprint('auth', __name__)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


@module_auth.route('/signin', methods=('POST',))
def signin():
    if not is_json_ajax():
        raise MethodNotAllowed()

    if current_user.is_authenticated:
        return '', 204

    signin_form = forms.SignIn(MultiDict(request.json))
    if not signin_form.validate():
        error_response = {}
        for field in signin_form.errors:
            error_response[field] = '. '.join(signin_form.errors[field])

        return jsonify(error_response), 400

    user = get_user_by_email(signin_form.email.data)
    if not check_password_hash(user.password, signin_form.password.data):
        return jsonify({'email': 'Неправильный логин или пароль'}), 400

    login_user(get_user_by_email(signin_form.email.data), remember=True)

    return '', 204


@module_auth.route('/signup', methods=('GET', 'POST'))
def signup():
    return_to = helpers.detect_return_route()

    if current_user.is_authenticated:
        return redirect(return_to)

    signup_form = forms.SignUp(helpers.build_signup_form_data())
    if request.method == 'POST' and signup_form.validate():
	new_user = User(
            name=signup_form.name.data,
            email=signup_form.email.data,
            password=generate_password_hash(signup_form.password.data),
            phone=signup_form.phone.data,
            address=signup_form.address.data
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(get_user_by_email(signup_form.email.data), remember=True)

        return redirect(return_to)

    return render_template(
        'modules/auth/signup.html',
        signup_form=signup_form
    )


@module_auth.route('/activate', methods=('GET',))
def activate():
    activate_token = request.args.get('token')
    if not activate_token:
        raise NotFound()

    # todo: login
    # todo: activate email

    return render_template('modules/auth/activate.html')


@module_auth.route('/restore/init', methods=('POST',))
def restore_init():
    if not is_json_ajax():
        raise MethodNotAllowed()

    restore_init_form = forms.RestoreInit(MultiDict(request.json))
    if not restore_init_form.validate():
        error_response = {}
        for field in restore_init_form.errors:
            error_response[field] = '. '.join(restore_init_form.errors[field])

        return jsonify(error_response), 400

    # todo: send restore email

    return '', 204


@module_auth.route('/restore', methods=('GET', 'POST'))
def restore():
    restore_token = request.args.get('token')
    if not restore_token:
        raise NotFound()

    restore_form = forms.Restore(request.form)
    if request.method == 'POST' and restore_form.validate():
        # todo: login
        # todo: move into cabinet
        # todo: reset restore token
        pass

    return render_template(
        'modules/auth/restore.html',
        restore_form=restore_form,
        restore_token=restore_token
    )


