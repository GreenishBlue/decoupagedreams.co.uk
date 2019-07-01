import os
from flask import Flask, render_template, Response, request, abort
from requests import get


app = Flask(__name__)


flags = {
  "ENABLE_BLOG": (os.environ.get("FLAG_ENABLE_BLOG") == "True"),
  "ENABLE_PRODUCTS": (os.environ.get("FLAG_ENABLE_PRODUCTS") == "True"),
  "ENABLE_INQUIRY": (os.environ.get("FLAG_ENABLE_INQUIRY") == "True"),
  "ENABLE_MAP": (os.environ.get("FLAG_ENABLE_MAP") == "True"),
  "ENABLE_GALLERY": (os.environ.get("FLAG_ENABLE_GALLERY") == "True"),
}

# The URL to the Google Apps Script service which to send emails to.
# Param: ?email=XXXXXXXXXX
APPS_SCRIPT_EMAIL_URL = "https://script.google.com/a/decoupagedreams.co.uk/macros/s/AKfycbxClyaeZUd5mjsdPYjWJqrmESeI9ch5BZdQ-k_5/exec"


def is_call_hours():
  """Check if we're currently within call hours.
  Weekdays from 8 AM to 6 PM."""
  from datetime import datetime, time
  import pytz
  now = datetime.now(pytz.timezone('Europe/London'))
  if time(8) <= now.time() <= time(18):
    return True 
  return False 


@app.route('/')
def home():
  return render_template('pages/index.html', flags=flags, call_hours=is_call_hours())


@app.route('/faq')
def landing_faq():
  return render_template('pages/faq.html', flags=flags, call_hours=is_call_hours())


@app.route('/occasions')
def landing_occasions():
  return render_template('pages/landing_occasions.html', flags=flags, call_hours=is_call_hours())


@app.route('/weddings')
def landing_weddings():
  return render_template('pages/landing_weddings.html', flags=flags, call_hours=is_call_hours())


@app.route('/gifts')
def landing_gifts():
  return render_template('pages/landing_gifts.html', flags=flags, posts=[], call_hours=is_call_hours())


@app.route('/blog')
def blog():
  return render_template('blog.html', flags=flags, posts=[], call_hours=is_call_hours())


@app.route('/blog/<string:post_id>')
def blog_post(post_id):
  return render_template('blog_post.html', flags=flags, post={}, call_hours=is_call_hours())


@app.route('/confirm_expanded')
def confirm_expanded():
  email_addr = request.args.get('email')
  if not email_addr:
    abort(500)
  name = request.args.get('name')
  if not name:
    name = ""
  message = request.args.get('message')
  if not message:
    message = ""
  budget = request.args.get('budget')
  if not budget:
    budget = ""
  print("New signup: " + email_addr)
  get(APPS_SCRIPT_EMAIL_URL + "?email=" + email_addr + "&name=" + name +
      "&message=" + message + "&budget=" + budget)
  return render_template('confirmed.html', flags=flags)


@app.route('/confirm')
def confirm():
  email_addr = request.args.get('email')
  if not email_addr:
    abort(500)
  print("New signup: " + email_addr)
  get(APPS_SCRIPT_EMAIL_URL + "?email=" + email_addr)
  return render_template('confirmed.html', flags=flags)


@app.route('/signup')
def signup():
  return render_template('signup.html', flags=flags)


@app.route('/gallery')
def gallery():
  return render_template('page_gallery.html', flags=flags)


@app.route('/build/bundle.css')
def build_css():
  """Request compiled CSS. This is only for development, and will be
  overridden by the Google App Engine config.
  
  Local Webpack server must be running via `npm start`"""
  return Response(get('http://localhost:8080/build/bundle.css').content, 
                  mimetype='text/css')


@app.route('/build/bundle.js')
def build_js():
  """Request compiled JS. This is only for development, and will be
  overridden by the Google App Engine config.
  
  Local Webpack server must be running via `npm start`"""
  return Response(get('http://localhost:8080/build/bundle.js').content, 
                  mimetype='application/javascript')


if __name__ == '__main__':
  app.run(debug=True)
