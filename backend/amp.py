from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


amp = Blueprint('amp', __name__, template_folder='templates')


@amp.route('/', defaults={'page': 'index'})
@amp.route('/<page>')
def show(page):
  try:
    return render_template('pages/amp_%s.html' % page)
  except TemplateNotFound:
    abort(404)


@amp.errorhandler(404)
def page_not_found(e):
    return render_template('pages/amp_404.html'), 404