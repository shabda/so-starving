import site
import os

# Django is such a pain to get to work within WSGI
here = os.path.dirname(os.path.abspath(__file__))
there = os.path.join(here, "fml")
site.addsitedir(here)
site.addsitedir(there)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 9002, application)
    print "Serving on port 8080..."
    httpd.serve_forever()
