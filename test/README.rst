In App Caching sucks
======================

Here is the gist of this.  I am not testing how fast the individual
frameworks are.  Comparing any of the frameworks to a cached page in
Varnish would be completely unfair. They are all running under the
worst case conditions. They are using using wsgiref.simple_server
and accessing high latency data.  These conditions would make any
framework cry.

I want to convey the fact that no matter how fast you get your
application layer is; If you are doing caching in the application is
going to be extremely slow compared to doing caching inside of a
specialized caching proxy like Varnish.  There is just no comparison.

The moral of the story is this.  Get your client side state out of
your server and into the client where it belong.

I'll leave you with this quote from RESTful web services::

    There’s an old joke. Patient: “Doctor, it hurts when I try to
    scale a system that keeps client state on the server!” Doctor:
    “Then don’t do that.” That’s the idea behind statelessness: don’t
    do the thing that causes the trouble.

Result Summary
---------------

Like I said before, do not use this to compare the frameworks to
themselves because frankly that would be unfair.



Unprimed
~~~~~~~~~
These values are basically skewed by the fact that the first request
have to fetch the data from Facebook

============== ==============
Framework      Mean req/sec   
============= ===============
webob+Varish           519.15
bottle                 236.07
flask                  149.99
django                  59.51
webpy                   24.88 
============= =============== 


Primed
~~~~~~~

============== ==============
Framework      Mean req/sec   
============= ===============
webob                 2436.18
bottle                 335.19
flask                  198.79
django                 121.02
webpy                   26.88
============= =============== 
