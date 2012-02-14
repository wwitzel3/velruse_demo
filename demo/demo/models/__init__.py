import transaction

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    return DBSession

# Database includes here allow for a simple programming API convention. By importing all the models here
# we can use the import models as M convention throughout the rest of the code.
from .user import User

# Explicit is better.
__all__ = [
    'DBSession',
    'initialize_sql',
    'User',
]

