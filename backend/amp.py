from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from htmlmin.main import minify


amp = Blueprint('amp', __name__, template_folder='templates')


def is_call_hours():
  """Check if we're currently within call hours.
  Weekdays from 8 AM to 6 PM."""
  from datetime import datetime, time
  import pytz
  now = datetime.now(pytz.timezone('Europe/London'))
  if time(8) <= now.time() <= time(18):
    return True 
  return False 


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
  nogtm = request.args.get('gtm') == 'false'
  is_landing_page = request.args.get('landing') == 'true'
  enable_fab = not is_landing_page and is_call_hours()
  enable_toolbar = not is_landing_page
  try:
    return render_template('pages/amp_%s.html' % page, enable_fab=enable_fab,
                           enable_toolbar=enable_toolbar, enable_gtm=not nogtm)
  except TemplateNotFound:
    abort(404)


@amp.errorhandler(404)
def page_not_found(e):
    return render_template('pages/amp_404.html'), 404