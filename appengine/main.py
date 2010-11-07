from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import urllib
import json as simplejson

class MainHandler(webapp.RequestHandler):
    def get(self):
        fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
        fb_data = memcache.get(key = fml_endpoint)
        if not fb_data:
            fb_response = urllib.urlopen(fml_endpoint,).read()
            fb_data = simplejson.loads(fb_response)["data"]
            memcache.add(key = fml_endpoint, value = fb_data, time = 30 * 60)
        self.response.out.write(template.render("templates/fml/index.html", {"data":fb_data}))

        #self.response.out.write('Hello world!')


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
