from __future__ import with_statement
from werkzeug.contrib.cache import SimpleCache
from nagare import component, presentation

import simplejson
import urllib

cache = SimpleCache()

class SoStarving(object):
    def get_fb_data(self):
        fml_endpoint = 'http://graph.facebook.com/search?q="so%20starving&type=post'
        fb_data = cache.get(key=fml_endpoint)
        if not fb_data:
            fb_response = urllib.urlopen(fml_endpoint,).read()
            fb_data = simplejson.loads(fb_response)["data"]
            cache.set(fml_endpoint, fb_data, 30 * 60)
        return fb_data


@presentation.render_for(SoStarving)
def render(self, h, *args):
    h << h.head.title(u'FMl')
    h << h.head.css(h.generate_id(), '''.author{ font-style:italic; }
li { list-style: none; }
.picture, .message { float: left; }''')
    with h.ul:
        for post in self.get_fb_data():
            with h.li:
                with h.div:
                    h << h.div(h.img(src='https://graph.facebook.com/'+post['from']['id']+'/picture'), class_='picture')
                    h << h.div(post.get('message', u''), u' : ', h.span(post['from']['name'], class_='author'), class_='message')
    return h.root

# ---------------------------------------------------------------

app = SoStarving
