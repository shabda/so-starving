import urllib
import json as simplejson

from pyramid.view import action
from beaker.cache import cache_region

class MyHandler(object):
    def __init__(self, request):
        self.request = request

    @action(renderer='index.mako')
    def index(self):
        fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
    
        @cache_region('short_term')   
        def fb_data(key=None):
            fb_response = urllib.urlopen(key,).read()
            return simplejson.loads(fb_response)["data"]
        
        return {'data': fb_data(fml_endpoint)}
