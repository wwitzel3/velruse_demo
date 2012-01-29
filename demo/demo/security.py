from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid

import demo.models as M

def groupfinder(userid, request):
    user = M.DBSession.query(M.User).get(userid)
    return [] if user else None

class RequestWithAttributes(Request):
    @reify
    def db(self):
        return M.DBSession()

    @reify
    def user(self):
        userid = unauthenticated_userid(self)
        if userid:
            return M.DBSession.query(M.User).get(userid)
        return None

