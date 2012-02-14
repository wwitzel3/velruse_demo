from hashlib import sha1
from datetime import datetime
from string import ascii_letters, digits
from random import choice

from pyramid.httpexceptions import HTTPForbidden

from sqlalchemy import (
    Column, Integer, Text,
    String, DateTime,
    )
from sqlalchemy.orm.exc import NoResultFound

from demo.models import Base, DBSession

# If you change this AFTER a user signed up they will not be able to
# login until they perform a password reset.
SALT = 'supersecretsalt'
CHARS = ascii_letters + digits
MAX_TRIES = 100

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True, index=True)
    email = Column(Text, unique=True)
    password = Column(String)
    signup_date = Column(DateTime, nullable=False, default=datetime.utcnow())

    identifier = Column(String, unique=True)

    twitter_id = Column(String, unique=True)
    twitter_auth_token = Column(String, unique=True)
    twitter_auth_secret = Column(String, unique=True)

    facebook_id = Column(String, unique=True)
    facebook_auth_token = Column(String, unique=True) 

    def __init__(self, *args, **kwargs):
        self.signup_date = datetime.utcnow().replace(microsecond=0)
        self.username = kwargs.get('username')
        if kwargs.get('password'):
            self.password = User.generate_password(kwargs.get('password'),
                    str(self.signup_date))
        self.email = kwargs.get('email', '{0}@example.com'.format(self.username))

    def update(self, *args, **kwargs):
        for k,v in kwargs.items():
            if k == 'password':
                v = User.generate_password(v, str(self.signup_date))
            setattr(self, k, v)

    @classmethod
    def social(cls, profile, credentials):
        # Grab out passed in values from end_point callback
        provider = profile.get('accounts')[0]
        identifier = sha1(provider.get('userid') + SALT).hexdigest()

        # Check if we already have a user with that identity?
        try:
            user = DBSession.query(cls).filter(cls.identifier==identifier).one()
            user.update_social_tokens(profile, credentials)
            return user
        except NoResultFound:
             pass

        # Get the username depending on the provider
        if provider.get('domain') == 'facebook.com':
            username = profile.get('preferredUsername', None)
        elif provider.get('domain') == 'twitter.com':
            username = profile.get('displayName', None)

        # Ensure the username is unique
        tries = 0
        while tries < MAX_TRIES:
            if not username:
                username = User.random_username(_range=7)
            if username:
                try:
                    DBSession.query(cls).filter(cls.username==username).one()
                    username = username + User.random_username(_range=3, prefix='_')
                except NoResultFound:
                    break
            tries += 1
        else:
            raise HTTPForbidden

        # Create the user, update the identifier, and socal tokens
        user = cls(username=username)
        user.identifier = identifier
        user.update_social_tokens(profile, credentials)

        return user

    def update_social_tokens(self, profile, credentials):
        provider = profile.get('accounts')[0]
        if provider.get('domain') == 'facebook.com':
            self.facebook_id = profile.get('preferredUsername')
            email = profile.get('verifiedEmail')
            if not DBSession.query(User).filter_by(email=email).count():
                self.email = profile.get('verifiedEmail')
            self.facebook_auth_token = credentials.get('oauthAccessToken')
        elif provider.get('domain') == 'twitter.com':
            self.twitter_id = profile.get('displayName')
            self.twitter_auth_token = credentials.get('oauthAccessToken')
            self.twitter_auth_secret = credentials.get('oauthAccessTokenSecret')

    @classmethod
    def authenticate(cls, login, password):
        from sqlalchemy import or_
        try:
            user = DBSession.query(cls).filter(or_(cls.username==login, cls.email==login)).one()
            password = User.generate_password(password, str(user.signup_date))
            if password == user.password:
                return user
            else:
                return None
        except NoResultFound:
            return None

    @staticmethod
    def generate_password(password, salt):
        password = sha1(password).hexdigest() + salt
        return sha1(password+SALT).hexdigest()

    @staticmethod
    def random_username(_range=5, prefix=''):
        return prefix + ''.join([choice(CHARS) for i in range(_range)])


