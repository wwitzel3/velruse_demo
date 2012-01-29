from pyramid.view import view_config
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render

from formencode import Invalid
from formencode import htmlfill

import demo.models as M
import demo.schema as S

@view_config(route_name='user.profile', renderer='user/profile.mako',
             request_method='GET')
def profile(request):
    user = request.db.query(M.User).filter_by(**request.matchdict).one()
    if not user:
        raise HTTPNotFound
    update_form = render('demo:templates/widgets/user/update.mako',
            dict(user=user))
    return dict(user=user, update_form=update_form)

@view_config(route_name='user.profile',  renderer='user/profile.mako',
             request_method='POST')
def profile_update(request):
    user = request.db.query(M.User).filter_by(**request.matchdict).one()
    try:
        clean_data = S.UserUpdateSchema(user=user).to_python(request.params)
        user.update(**clean_data)
        request.db.flush()
        return HTTPFound(location=route_url('user.profile', request,
                     username=user.username))
    except Invalid, e:
        e.value['password'] = ''
        e.value['password_verify'] = ''
        update_form = render('demo:templates/widgets/user/update.mako', dict(user=user))
        update_form = htmlfill.render(update_form, e.value, e.error_dict or {})

    return dict(user=user, update_form=update_form)

def user_routes(config):
    config.add_route('user.profile', '/{username}')

