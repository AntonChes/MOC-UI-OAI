from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from .http_login_trainer import auth_trainer


def construct_blueprint():
    thirdbot_page = Blueprint('thirdbot_page', __name__,
                            template_folder='templates')

    @thirdbot_page.route('/')
    @auth_trainer.login_required
    def thirdbot_page_all():
        from models import ThirdBot
        try:
            return render_template(f'thirdbot-page.html', third_bots = ThirdBot.query.all())
        except TemplateNotFound:
            abort(404)

    return thirdbot_page

