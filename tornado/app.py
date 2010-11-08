import tornado.httpserver
import tornado.ioloop
import tornado.web

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import simplejson
import urllib

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        #return
        fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
        fb_data = cache.get(key = fml_endpoint)
        if not fb_data:
            fb_response = urllib.urlopen(fml_endpoint,).read()
            fb_data = simplejson.loads(fb_response)["data"]
            cache.set(fml_endpoint, fb_data, 30 * 60)
        return self.render('templates/index.html', data=fb_data)

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()