from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.core.cache import cache

import urllib
import json as simplejson

def index(request):
    fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
    fb_data = cache.get(key = fml_endpoint)
    if not fb_data:
        fb_response = urllib.urlopen(fml_endpoint,).read()
        fb_data = simplejson.loads(fb_response)["data"]
        cache.set(fml_endpoint, fb_data, 30 * 60)
    return render_to_response("index.html", {"data": fb_data})

