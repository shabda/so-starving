import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import urllib

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
        fb_data = cache.get(key = self.fml_endpoint)
        if not fb_data:
            http = tornado.httpclient.AsyncHTTPClient()
            http.fetch(self.fml_endpoint, callback=self.on_response)

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        fb_data = tornado.escape.json_decode(response.body)["data"]
        cache.set(self.fml_endpoint, fb_data, 30 * 60)
        return self.render('templates/index.html', data=fb_data)


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()