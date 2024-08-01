import os
import sys

from sqlalchemy import create_engine

sys.path.append(os.path.abspath('.'))
SQLALCHEMY_DATABASE_URL = "sqlite:///./data.sqlite3"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


event.listen(engine, 'connect', _fk_pragma_on_connect)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
