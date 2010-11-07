# -*- coding: utf-8 -*- 

import urllib
from gluon.contrib.simplejson import loads

def index():
    endpoint='http://graph.facebook.com/search?q="so%20starving&type=post'
    def get_data(): return loads(urllib.urlopen(endpoint).read())['data']
    data = cache.ram(endpoint,get_data,30*60)
    return dict(data=data)
