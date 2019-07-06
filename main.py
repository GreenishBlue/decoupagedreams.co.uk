import os
from flask import Flask, render_template, Response, request, abort, redirect
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


collections = {
  "showcase": {
    "title": "Product Showcase",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris eget sem eu velit gravida placerat a quis nisl. Ut posuere sodales odio, eu consectetur sem dapibus et. Maecenas imperdiet bibendum pretium.",
    "meta_description": "collection meta description",
    "cta": "Make An Inquiry",
    "cta_url": "/contact",
    "cards": [
    ]
  }
}

import random
def generate_sample_image():
  width = random.randint(2, 4) * 100 
  height = random.randint(2, 6) * 100 
  return {
    "type": "image",
    "image": {
      "class": "mdc-image-list__image", # mdc-card
      "preview_src": "https://picsum.photos/%s/%s?blur=10" % (width, height),
      "src": "https://picsum.photos/%s/%s" % (width, height),
      "srcset": "https://picsum.photos/%s/%s 1x" % (width, height),
      "caption": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras in tincidunt eros.",
      "alt": "image alt",
      "width": width,
      "height": height,
    }
  }

def generate_sample_card():
  lipsums = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Aenean non enim metus. Quisque id nulla dolor.",
    "Fusce feugiat fermentum ligula, quis egestas risus elementum ut. Suspendisse fringilla vehicula libero, at fringilla sapien eleifend et."
  ]
  return {
    "type": "text",
    "caption": lipsums[random.randrange(len(lipsums))]
  }

for i in range(0, 5):
  collections["showcase"]["cards"].append(generate_sample_image())

for i in range(0, 5):
  pass
  # collections["showcase"]["cards"].append(generate_sample_card())

for i in range(0, 15):
  collections["showcase"]["cards"].append(generate_sample_image())

random.shuffle(collections["showcase"]["cards"])

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
def list_collections():
  return redirect('/gallery/showcase', 302) # temp until gallery list done
  return render_template('gallery_root.html', flags=get_flags(request),
                         call_hours=is_call_hours(), collections=collections, 
                         tags=tags)


@app.route('/gallery/<collection_id>')
def view_collection(collection_id):
  try:
    collection = collections[collection_id]
  except KeyError:
    abort(404)
  return render_template('gallery_collection.html', flags=get_flags(request), 
                         call_hours=is_call_hours(), collection=collection)


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
