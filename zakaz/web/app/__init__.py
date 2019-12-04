# hack for this stupid vds
import sys


import stripe
from flask import Flask, session, g
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager, current_user
from flask_htmlmin import HTMLMIN

# app
app = Flask(__name__)
app.config.from_object('app.config')

# db
db = SQLAlchemy(app)
db.init_app(app)

# assets
assets = Environment(app)
assets.init_app(app)

# csrf
CsrfProtect(app)

# migrate
migrate = Migrate(app, db)

# session
# Session(app)

# html min
html_min = HTMLMIN(app)

# login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user




# stripe
stripe.api_key = app.config['STRIPE_API_KEY']


# static module
from app.modules.static.views import module_static
app.register_blueprint(module_static)

# auth module
from app.modules.auth.views import module_auth
app.register_blueprint(module_auth, url_prefix='/auth')

# services module
from app.modules.services.views import module_services
app.register_blueprint(module_services, url_prefix='/services')

# cabinet module
from app.modules.cabinet.views import module_cabinet
app.register_blueprint(module_cabinet, url_prefix='/cabinet')

# page module
from app.modules.page.views import module_page
app.register_blueprint(module_page)

# catalogue module
from app.modules.catalogue.views import module_catalogue
app.register_blueprint(module_catalogue, url_prefix='/catalogue')

# admin module
from app.modules.admin import init_admin_module
init_admin_module(app)

