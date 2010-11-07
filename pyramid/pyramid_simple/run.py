import urllib
import json as simplejson

from pyramid.configuration import Configurator
from paste.httpserver import serve

from beaker.cache import cache_regions, cache_region
cache_regions['short_term'] = dict(type='memory', expire=30*60)

def index(request):
    fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
    
    @cache_region('short_term')   
    def fb_data(key=None):
        fb_response = urllib.urlopen(key,).read()
        return simplejson.loads(fb_response)["data"]
        
    return {'data': fb_data(fml_endpoint)}

if __name__ == '__main__':
    settings = {}
    settings['mako.directories'] = './templates'
    config = Configurator(settings=settings)
    config.begin()
    config.add_view(index, name='', renderer='index.mako')
    config.end()
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')