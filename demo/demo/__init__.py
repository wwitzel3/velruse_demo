from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config

import demo.models as M
from demo.security import RequestWithAttributes
from demo.security import groupfinder

from demo.views.default import default_routes
from demo.views.user import user_routes

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    authn_p = AuthTktAuthenticationPolicy(secret='demo-secret', callback=groupfinder)
    authz_p = ACLAuthorizationPolicy()
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    engine = engine_from_config(settings, 'sqlalchemy.')
    config = Configurator(
        settings=settings,
        session_factory=session_factory,
        request_factory=RequestWithAttributes,
        authentication_policy=authn_p,
        authorization_policy=authz_p,
    )
    config.begin()
    ## Database
    config.scan('.models')
    M.initialize_sql(engine)

    ## Routing & Views
    config.include(default_routes, route_prefix='')
    config.include(user_routes, route_prefix='/user')

    ## Velruse Auth
    config.include('velruse.providers.facebook')
    config.include('velruse.providers.twitter')

    config.add_facebook_login(
        settings['velruse.facebook.app_id'],
        settings['velruse.facebook.app_secret'],
        settings['velruse.facebook.scope'])

    config.scan('.views')
    config.add_static_view('static', 'demo:static')

    config.end()
    return config.make_wsgi_app()

