import os
from flask import Flask, render_template, Response, request
from requests import get


app = Flask(__name__)


FLAG_ENABLE_HEADER = "FLAG_ENABLE_HEADER"
flags = {
  "ENABLE_HEADER": (os.environ.get(FLAG_ENABLE_HEADER) == "True"),
}

# The URL to the Google Apps Script service which to send emails to.
# Param: ?email=XXXXXXXXXX
APPS_SCRIPT_EMAIL_URL = "https://script.google.com/a/decoupagedreams.co.uk/macros/s/AKfycbxClyaeZUd5mjsdPYjWJqrmESeI9ch5BZdQ-k_5/exec"


@app.route('/')
def home():
  return render_template('index.html', flags=flags)


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
