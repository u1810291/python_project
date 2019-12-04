from flask import Blueprint, render_template
from app.models import Page
import markdown

module_page = Blueprint('page', __name__)


@module_page.route('/<slug>', methods=('GET',))
def render(slug):
    page = Page.query.filter_by(slug=slug).first()
    if page is None:
        return 'Not Found', 404

    page.content = markdown.markdown(page.content)

    return render_template(
        'modules/page/render.html',
        page=page
    )
