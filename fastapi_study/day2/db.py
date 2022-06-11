# pylint: disable=wildcard-import,unused-import,unused-wildcard-import

from datetime import datetime, timezone, timedelta
from sqlalchemy import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import *
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.exc import *
from sqlalchemy.orm.session import make_transient, Session
from sqlalchemy.sql import functions as funcs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

from fastapi import Depends
from fastapi_study.day2.settings import Settings, use_settings


BaseModel = declarative_base()

_factories = {}


def get_session_factory(dsn, cls=BaseModel, echo=False):
    """returns cached sqlalchemy scoped session factory"""
    if dsn not in _factories:
        engine = create_engine(dsn, encoding='utf8', echo=echo)
        factory = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False, bind=engine))
        cls.metadata.create_all(bind=engine)
        cls.query = factory.query_property()
        _factories[dsn] = factory
    return _factories.get(dsn)


def use_db(settings: Settings = Depends(use_settings)):
    """injects sqlalchemy scoped session dependency"""
    SessionFactory = get_session_factory(settings.database_dsn)
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()

