# pylint: disable=wildcard-import,unused-import,unused-wildcard-import

from datetime import datetime, timezone, timedelta
from asyncio import current_task
from sqlalchemy import *
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import *
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.exc import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session
from sqlalchemy.orm.session import make_transient, Session
from sqlalchemy.sql import functions as funcs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

from fastapi import Depends
from fastapi_study.day2.settings import Settings, use_settings

# aliases
op = type('op', (object,), {'insert': insert, 'select': select,
                            'update': update, 'delete': delete})

BaseModel = declarative_base()

_factories = {}


async def get_session_factory(dsn, *, cls=BaseModel, echo=False):
    """returns cached sqlalchemy async_scoped_session factory"""
    if dsn not in _factories:
        engine = create_async_engine(dsn, encoding='utf8', echo=echo)
        factory = async_scoped_session(sessionmaker(autocommit=False,
                                                    expire_on_commit=False,
                                                    class_=AsyncSession,
                                                    autoflush=False, bind=engine),
                                       scopefunc=current_task)

        async with engine.begin() as conn:
            await conn.run_sync(cls.metadata.create_all)

        _factories[dsn] = factory
    return _factories.get(dsn)


async def use_db(settings: Settings = Depends(use_settings)):
    """injects sqlalchemy async_scoped_session dependency"""
    SessionFactory = await get_session_factory(settings.database_dsn)
    async with SessionFactory() as session:
        yield session
