from flask import Blueprint, render_template
from app.models import Tag, Shop
from sqlalchemy import asc

module_catalogue = Blueprint('catalogue', __name__)


@module_catalogue.route('/', methods=('GET',))
def index():
    tags = Tag.query.order_by(asc(getattr(Tag, 'weight'))).all()
    shops = Shop.query.order_by(asc(getattr(Shop, 'weight'))).all()

    return render_template(
        'modules/catalogue/index.html',
        tags=tags,
        shops=shops,
    )
