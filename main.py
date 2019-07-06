import os
from flask import Flask, render_template, Response, request, abort
from requests import get


app = Flask(__name__)


flags = {
  "ENABLE_BLOG": (os.environ.get("FLAG_ENABLE_BLOG") == "True"),
  "ENABLE_PRODUCTS": (os.environ.get("FLAG_ENABLE_PRODUCTS") == "True"),
  "ENABLE_GTM": (os.environ.get("FLAG_ENABLE_GTM") == "True"),
}


URLLIST_PATHS = [
  '/',
  '/weddings',
  '/faq',
  '/contact',
]


# The URL to the Google Apps Script service which to send emails to.
# Param: ?email=XXXXXXXXXX
APPS_SCRIPT_EMAIL_URL = "https://script.google.com/a/decoupagedreams.co.uk/macros/s/AKfycbxClyaeZUd5mjsdPYjWJqrmESeI9ch5BZdQ-k_5/exec"


products = [
  {
    "photo_url": "https://images.unsplash.com/photo-1519741497674-611481863552?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
    "label": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ut dui mattis, pellentesque augue vel, rhoncus lacus."
  },

  {
      "photo_url": "https://images.unsplash.com/photo-1521543832500-49e69fb2bea2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2134&q=80",
    "label": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ut dui mattis, pellentesque augue vel, rhoncus lacus."
  },

  {
      "photo_url": "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
    "label": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ut dui mattis, pellentesque augue vel, rhoncus lacus."
  },
] 


tags = [
  "Centrepiece",
  "Chair Cover",
  "Sash",
  "Favour Box",
  "Stationery",
  "Table Decoration",
  "Card",
  "Wedding",
  "Invitation",
  "Extras",
  "Venue Dressing",
  "Table Plan"
] 

import random
random.shuffle(tags)


def is_call_hours():
  """Check if we're currently within call hours.
  Weekdays from 8 AM to 6 PM."""
  from datetime import datetime, time
  import pytz
  now = datetime.now(pytz.timezone('Europe/London'))
  if time(8) <= now.time() <= time(18):
    return True 
  return False 



def get_flags(request):
  nogtm = request.args.get('nogtm')
  if nogtm == str(1):
    my_flags = dict(flags) # copy dict
    my_flags['ENABLE_GTM'] = False
    return my_flags
  else:
    return flags


@app.route('/')
def home():
  return render_template('pages/index.html', flags=get_flags(request), 
                         call_hours=is_call_hours())


@app.route('/gallery')
def list_products():
  return render_template('products.html', flags=get_flags(request),
                         call_hours=is_call_hours(), products=products, tags=tags)


@app.route('/gallery/<product_id>')
def view_product(product_id):
  product = products[product_id]
  return render_template('view_product.html', flags=get_flags(request), 
                         call_hours=is_call_hours(), product=product)


@app.route('/faq')
def landing_faq():
  return render_template('pages/faq.html', flags=get_flags(request), 
                         call_hours=is_call_hours())


@app.route('/occasions')
def landing_occasions():
  return render_template('pages/landing_occasions.html', flags=get_flags(request), 
                         call_hours=is_call_hours())


@app.route('/weddings')
def landing_weddings():
  return render_template('pages/landing_weddings.html', flags=get_flags(request), 
                         call_hours=is_call_hours())


@app.route('/gifts')
def landing_gifts():
  return render_template('pages/landing_gifts.html', flags=get_flags(request),  
                         posts=[], call_hours=is_call_hours())


@app.route('/faq')
def faq():
  return render_template('faq.html', flags=get_flags(request), 
                         call_hours=is_call_hours())


@app.route('/blog')
def blog():
  return render_template('blog.html', flags=get_flags(request), 
                         posts=[], call_hours=is_call_hours())


@app.route('/blog/<string:post_id>')
def blog_post(post_id):
  return render_template('blog_post.html', flags=get_flags(request),
                         post={}, call_hours=is_call_hours())


@app.route('/contact')
def contact():
  return render_template('contact.html', flags=get_flags(request),
                         call_hours=is_call_hours())


@app.route('/urllist.txt')
def urlist():
  url_prefix = 'https://www.decoupagedreams.co.uk'
  generated = ''
  for path in URLLIST_PATHS:
    generated += url_prefix
    generated += path
    generated += '\n'
  from flask import Response
  return Response(generated, mimetype='text/plain')


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


@app.route('/dist/build/bundle.css')
def build_css():
  """Request compiled CSS. This is only for development, and will be
  overridden by the Google App Engine config.
  
  Local Webpack server must be running via `npm start`"""
  return Response(get('http://localhost:8080/build/bundle.css').content, 
                  mimetype='text/css')


@app.route('/dist/build/bundle.js')
def build_js():
  """Request compiled JS. This is only for development, and will be
  overridden by the Google App Engine config.
  
  Local Webpack server must be running via `npm start`"""
  return Response(get('http://localhost:8080/build/bundle.js').content, 
                  mimetype='application/javascript')


if __name__ == '__main__':
  app.run(debug=True)
