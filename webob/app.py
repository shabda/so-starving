from webob import Response, exc
from webob.dec import  wsgify
from jinja2 import FileSystemLoader, Environment
from datetime import datetime, timedelta
import urllib
import json as simplejson


@wsgify
def index(request):
    if request.path != "/":
        raise exc.HTTPNotFound()

    # Fetch data
    fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
    fb_response = urllib.urlopen(fml_endpoint).read()
    fb_data = simplejson.loads(fb_response)["data"]

    # Render the content
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("index.html")
    body = template.render(data = fb_data)
    
    # Set the body and the cache expiration
    response = Response(body=body)
    response.cache_expires(seconds=30 * 60)

    # Return it the response; we can now put a proper web cache in front of
    # our service.  Even if we don't, every HTTP client with a cache becomes
    # a replicated node for this resource.  How's that for horizontal scaling?
    return response


application = index

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 9008, application)
    print "Serving on port 9008..."
    httpd.serve_forever()
