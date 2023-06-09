from flask import Blueprint, render_template

err_page = Blueprint('err_page', __name__,)

@err_page.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@err_page.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500