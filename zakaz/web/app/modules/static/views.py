from flask import Blueprint, render_template

module_static = Blueprint('static', __name__)


@module_static.route('/', methods=('GET',))
def index():
    return render_template('modules/static/index.html')


@module_static.route('/about', methods=('GET',))
def about():
    return render_template('modules/static/about.html')

