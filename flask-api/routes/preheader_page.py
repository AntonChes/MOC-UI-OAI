from flask import Blueprint, request, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from .http_login_trainer import auth_trainer


def construct_blueprint(db,):
    preheader_page = Blueprint('preheader_page', __name__,
                            template_folder='templates')

    @preheader_page.route('/')
    @auth_trainer.login_required
    def preheader_page_all():
        from models import PreHeader
        try:
            return render_template(f'preheader-page-all.html', preheaders = PreHeader.query.all())
        except TemplateNotFound:
            abort(404)

    @preheader_page.route('/add', methods=['GET', 'POST'])
    @auth_trainer.login_required
    def preheader_page_add():
        from models import PreHeader

        if request.method == 'POST':
            search_entry = PreHeader.query.filter_by(full_name=request.form['name']).first()
            if search_entry:
                search_entry.full_name = request.form['name']
                search_entry.content = request.form['content']
                search_entry = db.session.merge(search_entry)
                db.session.add(search_entry)
                db.session.commit()
            else:
                preheader = PreHeader(request.form['name'], request.form['content'])
                db.session.add(preheader)
                db.session.commit()

            return redirect(url_for('preheader_page.preheader_page_all'))
        return render_template('preheader-page-add.html')

    # todo | error
    @preheader_page.route('/remove/<int:preheader_id>')
    @auth_trainer.login_required
    def preheader_page_remove(preheader_id=None):
        from models import PreHeader

        try:
            search_entry = PreHeader.query.get_or_404(preheader_id)
            db.session.delete(search_entry)
            db.session.commit()
            return render_template(f'preheader-page-all.html', preheaders = PreHeader.query.all())
        except TemplateNotFound:
            abort(404)

    return preheader_page

