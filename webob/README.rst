This demonstration separates the concerns of caching and request
processing and lets the appropriate layer handle it.  

HTTP/1.1 defines headers to describe how your content can be cached.
You could let your clients handle the caching and distribute your
caching layer across all clients requesting your data.  This makes
every browser in your audience a node in a massively distributed cache
layer and you didn't have to pay Amazon a dime to roll out a single
node.

If you don't like trusting clients to be your cache, you can setup
something like varnish to be a caching proxy between your server and
your users.

I have provided a really simple varnish configuration file and launcher script.

If you are on Ubuntu simply do::

  sudo apt-get install varnish

The default configuration of varnish uses the backend address
127.0.0.1:8000 which is what I have configured my WSGI application to use.
