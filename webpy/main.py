import web

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import urllib
import json as simplejson

urls = (
  '/', 'index'
)

class index:
    def GET(self):
            fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
            fb_data = cache.get(key=fml_endpoint)
            if not fb_data:
                fb_response = urllib.urlopen(fml_endpoint,).read()
                fb_data = simplejson.loads(fb_response)["data"]
                cache.set(fml_endpoint, fb_data, 30 * 60)
            index = web.template.frender('templates/index.html')
            return index(fb_data)


app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
