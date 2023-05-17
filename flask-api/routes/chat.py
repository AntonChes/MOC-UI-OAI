from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from .http_login import auth

chat_page = Blueprint('chat_page', __name__,
                        template_folder='templates')

@chat_page.route('/')
@auth.login_required
def chat_route():
    try:
        return render_template(f'chat.html')
    except TemplateNotFound:
        abort(404)