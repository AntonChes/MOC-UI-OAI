from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from .http_login import auth

chat_advanced_page = Blueprint('chat_advanced_page', __name__,
                        template_folder='templates')

@chat_advanced_page.route('/advanced')
@auth.login_required
def chat_route():
    try:
        return render_template(f'chat-advanced.html')
    except TemplateNotFound:
        abort(404)