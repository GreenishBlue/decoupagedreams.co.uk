from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from htmlmin.main import minify


amp = Blueprint('amp', __name__, template_folder='templates')


@amp.after_request
def response_minify(response):
  """
  minify html response to decrease site traffic
  """
  if response.content_type == u'text/html; charset=utf-8':
    response.set_data(
      minify(response.get_data(as_text=True))
    )

    response.data = response.data.replace(b'<style>', b'<style amp-custom>')
    return response
  return response


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