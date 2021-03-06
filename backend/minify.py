# MIT License

# Copyright (c) 2017 Mohamed Feddad
# Copyright (c) 2019 Cameron Brown

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from flask import request
from lesscpy import compile
from jsmin import jsmin
from six import StringIO
from htmlmin import minify as minifyHtml
from hashlib import md5

"""Adapted from flask_minify to support AMP. minify seeks <style> tags with 
matching names for both start/end tags, wheras AMP's opening tag is defined
as <style amp-custom></style>. For this reason we need to control the order
that content is stripped out."""
class minify(object):
  def __init__(
    self, app=None,
    html=True, js=True,
    cssless=True, cache=True,
    fail_safe=True, bypass=[]
  ):
    """
    A Flask extension to minify flask response for html,
    javascript, css and less.
    @param: app Flask app instance to be passed (default:None).
    @param: js To minify the css output (default:False).
    @param: cssless To minify spaces in css (default:True).
    @param: cache To cache minifed response with hash (default: True).
    @param: fail_safe to avoid raising error while minifying (default True)
    @param: bypass a list of the routes to be bypassed by the minifer
    """
    self.app = app
    self.html = html
    self.js = js
    self.cssless = cssless
    self.cache = cache
    self.fail_safe = fail_safe
    self.bypass = bypass
    self.history = {}  # where cache hash and compiled response stored
    self.hashes = {}  # where the hashes and text will be stored
    if self.app is None:
      raise(AttributeError("minify(app=) requires Flask app instance"))
    for arg in ['cssless', 'js', 'html', 'cache']:
      if not isinstance(eval(arg), bool):
        raise(TypeError("minify(" + arg + "=) requires True or False"))
    self.app.after_request(self.toLoopTag)

  def process_response(self, response):
    return self.toLoopTag(response)

  def getHashed(self, text):
    """ to return text hashed and store it in hashes """
    if text in self.hashes.keys():
      return self.hashes.get(text)
    else:
      hashed = md5(text.encode('utf8')).hexdigest()[:9]
      self.hashes[text] = hashed
      return hashed

  def storeMinifed(self, css, text, toReplace):
    """ to minify and store in history with hash key """
    if self.cache and self.getHashed(text) in self.history.keys():
      return self.history[self.getHashed(text)]
    else:
      minifed = compile(
          StringIO(toReplace), minify=True, xminify=True
      ) if css else jsmin(toReplace).replace('\n', ';')
      if self.cache and self.getHashed(text) not in self.history.keys():
        self.history[self.getHashed(text)] = minifed
      return minifed

  def toLoopTag(self, response):
    if response.content_type == u'text/html; charset=utf-8' and not (
      request.url_rule.rule in self.bypass
    ):
      response.direct_passthrough = False
      text = response.get_data(as_text=True)
      for tag in [t for t in [
        (0, 'style')[self.cssless],
        (0, 'script')[self.js]
      ] if t != 0]:
        if '<' + tag + ' type=' in text or '<' + tag + '>' in text:
          for i in range(1, len(text.split('<' + tag))):
            toReplace = text.split(
              '<' + tag, i
            )[i].split(
              '</' + tag + '>'
            )[0].split(
              '>', 1
            )[1]
            result = None
            try:
              result = text.replace(
                toReplace,
                self.storeMinifed(
                  tag == 'style', text, toReplace)
              ) if len(toReplace) > 2 else text
              text = result
            except Exception as e:
              if self.fail_safe:
                text = result or text
              else:
                raise e
      finalResp = minifyHtml(text) if self.html else text
      response.set_data(finalResp)
    return response