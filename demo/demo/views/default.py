from velruse.store.sqlstore import KeyStorage

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.renderers import render
from pyramid.security import forget
from pyramid.security import remember
from pyramid.security import unauthenticated_userid
from pyramid.view import view_config
from pyramid.url import route_url

import json

from formencode import Invalid
from formencode import htmlfill

import demo.models as M
import demo.schema as S

@view_config(route_name='index', renderer='default/index.mako')
def index(request):
    return dict(userid=unauthenticated_userid(request))

@view_config(route_name='login', renderer='default/login.mako')
def login(request):
    login_form = render('demo:templates/widgets/login.mako', {},
            request=request)
    signup_form = render('demo:templates/widgets/signup.mako', {},
            request=request)

    if 'form.login' in request.params:
        try:
            clean_data = S.UserLoginSchema().to_python(request.params)
            user = M.User.query.get(_id=clean_data.get('userid'))
            headers = remember(request, user.id)
            return HTTPFound(location=route_url('user.profile', request,
                             username=user.username), headers=headers)
        except Invalid, e:
            e.value['password'] = ''
            login_form = htmlfill.render(login_form, e.value, e.error_dict or {})

    elif 'form.signup' in request.params:
        try:
            clean_data = S.UserSignupSchema().to_python(request.params)
        except Invalid, e:
            e.value['password'] = ''
            e.value['password_verify'] = ''
            signup_form = htmlfill.render(signup_form, e.value, e.error_dict or {})
        else:
            user = M.User(**request.params)
            M.DBSession.add(user)
            M.DBSession.flush()
            headers = remember(request, user.id)
            return HTTPFound(location=route_url('user.profile', request,
                             username=user.username), headers=headers)
    elif 'token' in request.params:
        key = request.params.get('token')
        storage = M.DBSession.query(KeyStorage).get(key)
        values = json.loads(storage.value)
        user = M.User.social(**values)
        if user:
            M.DBSession.add(user)
            M.DBSession.flush()
            headers = remember(request, user.id)
            return HTTPFound(location=route_url('user.profile', request,
                username=user.username), headers=headers)

    return dict(
        signup_form=signup_form,
        login_form=login_form
    )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=route_url('index', request),
                     headers=headers)

@view_config(context=HTTPForbidden, renderer='default/forbidden.mako')
def forbidden(request):
    return dict()

def default_routes(config):
    config.add_route('index', '')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

