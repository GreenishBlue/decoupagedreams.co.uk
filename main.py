from flask import Flask, render_template, Response
from requests import get


app = Flask(__name__)


@app.route('/')
def home():
  return render_template('index2.html')


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
