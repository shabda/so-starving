from pyroutes import route, settings, application
from pyroutes.http.response import Response
from pyroutes.template import TemplateRenderer
import memcache
import simplejson
import urllib

tr = TemplateRenderer()
cache = memcache.Client(servers=['127.0.0.1:11211'])

@route('/')
def index(request):
    fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
    fb_data = cache.get(fml_endpoint)
    if not fb_data:
        fb_response = urllib.urlopen(fml_endpoint).read()
        fb_data = simplejson.loads(fb_response)['data']
        cache.set(fml_endpoint, fb_data)
    return Response(tr.render('base.xml',
        {'ul': [
            {'li': {
                '#picture': {'img/src': 'https://graph.facebook.com/%s/picture' % post['from']['id']},
                '#message': {'#msg': post['message'], '#author': post['from']['name']}
                   }
            }
            for post in [p for p in fb_data if 'message' in p]]
        }))

if __name__ == '__main__':
    from pyroutes.utils import devserver
    devserver(application)
