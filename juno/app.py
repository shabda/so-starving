from juno import *

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import urllib
import json as simplejson

@route('/')
def index(web):
    fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
    fb_data = cache.get(key = fml_endpoint)
    if not fb_data:
        fb_response = urllib.urlopen(fml_endpoint,).read()
        fb_data = simplejson.loads(fb_response)["data"]
        cache.set(fml_endpoint, fb_data, 30 * 60)
    return template('index.html', {"data": fb_data})



if __name__ == '__main__':
    config("auto_reload_templates", True)
    config('use_debugger', True)
    run(mode = "dev")