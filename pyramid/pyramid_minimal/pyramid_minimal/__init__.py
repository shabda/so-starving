from pyramid_beaker import session_factory_from_settings

from beaker.cache import cache_regions
cache_regions['short_term'] = dict(type='memory', expire=30*60)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from pyramid.configuration import Configurator
    config = Configurator(settings=settings)
    config.begin()
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    config.add_static_view('static', 'pyramid_minimal:static/')
    config.add_handler('action', '/{action}', 'pyramid_minimal.handlers:MyHandler')
    config.add_handler('home', '/', 'pyramid_minimal.handlers:MyHandler',
                       action='index')
    config.add_subscriber('pyramid_minimal.subscribers.add_renderer_globals',
                          'pyramid.events.BeforeRender')
    config.end()
    return config.make_wsgi_app()

