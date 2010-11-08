from flask import Flask
from flask import render_template

import urllib
import json as simplejson

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)

@app.route('/')
def index():
        fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
        fb_data = cache.get(key=fml_endpoint)
        if not fb_data:
            fb_response = urllib.urlopen(fml_endpoint,).read()
            fb_data = simplejson.loads(fb_response)["data"]
            cache.set(fml_endpoint, fb_data, 30 * 60)
        return render_template("index.html", data=fb_data)

application = app

if __name__ == '__main__':
    app.debug = True
    app.run()
