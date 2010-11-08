import sys
from multiprocessing import Process
import time
from runserver import runserver
import os
import logging
import subprocess
import urllib


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

here = os.path.dirname(os.path.abspath(__file__))
there = os.path.join(here, "../")

def h(filename):
    return os.path.join(here, filename)

def t(filename):
    return os.path.join(there, filename)


def runcommand(cmd):
    """Returns the output of a command"""
    p = subprocess.Popen(cmd, shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    errors = p.stderr.read()
    result = p.stdout.read()
    ret = p.wait()

    if ret != 0:
        raise Exception(errors)

    return result


def abtest(url):
    result = runcommand('ab -n 1000 -c 1 %s' % url)

    return result


SERVERS = (
    #('bottle', "bottle/app.py"),
    #('django', "django/app.py"),
    #('flask', "flask/app.py"),
    # pyramid keeps dying on midtest, screw it
    #('pyramid', "pyramid/run.py"),
    ('webpy', "webpy/main.py"),
    # Make sure you start varnish on port 10002 first
    ('webob', "webob/app.py"),
)

def main():
    for framework, module_filename in SERVERS:
        if framework == "webob":
            # The webob WSGI app needs to be on port 9008 so that
            # Varnish can talk to it but apache bench will talk to the service
            # through Varnish on port 10002.  It's on port 10002 so we can
            # have it running before the test without clobbering the other
            # servers
            port = 9008
            uri = "http://localhost:10002/"
        else:
            uri = "http://localhost:10001/"
            port = 10001



        log.info("Starting the %s server" % (framework, ))
        server = Process(target=runserver, args=(t(module_filename), "localhost",
                                               port))

        server.start()

        # wait for everything to come up
        log.info("Waiting 5 seconds for the server to come up")
        time.sleep(5)

        log.info("Running the unprimed test")
        unprimed = abtest(uri)
        print >> sys.stderr, unprimed

        log.info("Running the primed test")
        primed = abtest(uri)
        print >> sys.stderr, primed

        log.info("Dumping the HTML of the server for debugging")
        with open(h("results/%s.html" % (framework, )), "w") as fh:
            fh.write(urllib.urlopen(uri).read())
        
        log.info("Shutting down the %s server" % (framework, ))
        server.terminate()

        primed_filename = os.path.join(here, "results/primed/%s.txt"\
                                           % (framework, ))
        unprimed_filename = os.path.join(here, "results/unprimed/%s.txt"
                                         % (framework, ))

        with open(unprimed_filename, "w") as fh:
            fh.write(unprimed)

        with open(primed_filename, "w") as fh:
            fh.write(primed)


if __name__ == '__main__':
    main()
