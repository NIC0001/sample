# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE = 'mysql+mysqlconnector://%s:%s@%s/%s' % (
    "user_name",
    "pass",
    "host:port",
    "db_name",
)
ENGINE = create_engine(
    DATABASE,
    echo=False
)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)
Base = declarative_base()
Base.query = session.query_property()
