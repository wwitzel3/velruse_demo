from formencode import Schema
from formencode import Invalid
from formencode import validators as v

from .validators import UniqueEmail
from .validators import UniqueUsername
from .validators import ValidUser

class UserUpdateSchema(Schema):
    '''
    Validate the user update form. Works with UniqueEmail
    to ensure no two users can have the same email address.
    '''
    def __init__(self, user):
        self._user = user

        self.allow_extra_fields = True
        self.username = v.String(not_empty=True)
        self.email = v.Email(resolve_domain=False, not_empty=True)
        self.password = v.String(if_missing=None)
        self.password_verify = v.String(if_missing=None)

        self.chained_validators = [
            v.FieldsMatch('password', 'password_verify'),
            UniqueEmail(self._user),
            UniqueUsername(self._user),
        ]

class UserLoginSchema(Schema):
    allow_extra_fields = True
    login = v.String(not_empty=True)
    password = v.String(not_empty=True)

    chained_validators = [
        ValidUser(),
    ]

class UserSignupSchema(Schema):
    '''
    Validate the user sign up form. Works with UniqueEmail
    to ensure no two users can have the same email address.
    '''
    allow_extra_fields = True
    username = v.String(not_empty=True)
    email = v.Email(resolve_domain=False, not_empty=True)
    password = v.String(not_empty=True)
    password_verify = v.String(not_empty=True)

    chained_validators = [
        v.FieldsMatch('password', 'password_verify'),
        UniqueEmail(),
        UniqueUsername(),
    ]

