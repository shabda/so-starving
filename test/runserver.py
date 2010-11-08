import imp
import sys
import multiprocessing
from wsgiref.simple_server import make_server
import logging
import os
from StringIO import StringIO


log = logging.getLogger(__name__)

def runserver(filename, host, port):
    there = os.path.dirname(filename)
    os.chdir(there)

    app = imp.load_module("app", open(filename, "r"), filename, 
                          ('.py', 'U', 1))
    log.info("running %s at %s:%s" % (filename, host, port))
    httpd = make_server(host, port, app.application)
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    try:
        httpd.serve_forever()
    except Exception:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        raise

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

