#!/usr/bin/env python
"""http://agiliq.com/blog/2010/11/i-am-so-starving-same-web-app-in-various-python-we/

The app(s) talks to Facebook, and finds out recent people who have
posted a public status with the text "so starving".

http://localhost:8880/
"""
from twisted.internet import reactor, defer
from twisted.python   import log
from twisted.web      import client, resource, server

from jinja2 import FileSystemLoader, Environment

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import json as simplejson

class StarvingResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        d = defer.maybeDeferred(self._render_GET, request)
        d.addCallbacks(request.write, request.processingFailed)
        d.addBoth(self._finishRequest, request)
        request.notifyFinish().addBoth(self._cancelRequest, request)
        return server.NOT_DONE_YET

    @defer.inlineCallbacks
    def _render_GET(self, request):
        fml_endpoint = 'http://graph.facebook.com/search?q=%22so%20starving%22&type=post'
        fb_data = cache.get(key=fml_endpoint)
        if not fb_data:
            fb_response = yield client.getPage(fml_endpoint)
            fb_data = simplejson.loads(fb_response)["data"]
            cache.set(fml_endpoint, fb_data, 30 * 60)
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template("index.html").render
        defer.returnValue(template(data=fb_data).encode('utf-8'))

    def _cancelRequest(self, unused, request):
        request.finish = lambda: None

    def _finishRequest(self, unused, request):
        request.finish()


if __name__=="__main__":
    import sys
    log.startLogging(sys.stderr)
    resource = StarvingResource()
    reactor.listenTCP(8880, server.Site(resource))
    reactor.run()
