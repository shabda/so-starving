from itty import get, run_itty
from jinja2 import FileSystemLoader, Environment

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import urllib
import json as simplejson


@get('/')
def index(request):
    fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
    fb_data = cache.get(key = fml_endpoint)
    if not fb_data:
        fb_response = urllib.urlopen(fml_endpoint,).read()
        fb_data = simplejson.loads(fb_response)["data"]
        cache.set(fml_endpoint, fb_data, 30 * 60)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("index.html")
    return template.render(data = fb_data)

run_itty()