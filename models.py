import os
from atexit import register
from typing import Type

from cachetools import cached
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import EmailType

import config

Base = declarative_base()


class Ads(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    autor = Column(Integer, ForeignKey("ads_users.id", ondelete="CASCADE"))


class User(Base):
    __tablename__ = "ads_users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(60), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


@cached({})
def get_engine():
    return create_engine(config.PG_DSN)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine())


def init_db():
    Base.metadata.create_all(bind=get_engine())


def close_db():
    get_engine().dispose()


ORM_MODEL_CLS = Type[User] | Type[Ads]
ORM_MODEL = User | Ads
