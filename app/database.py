# imports ------>
# the engine use to interact with postgres.
from sqlalchemy import create_engine
# define table mapping, instead of baseModel
from sqlalchemy.ext.declarative import declarative_base
# to make read/write opeartions with postgres.
from sqlalchemy.orm import sessionmaker

import time
# make the connection and execute operations with postgreSql database .
import psycopg2
from psycopg2.extras import RealDictCursor

from .config import settings


# notes: ------>
# in this database file, would hanle the connection/operations with database, using [SqlAlchemy]
# with it's driver [psycopg2]


# url :
# 'postgresql://<username>:<password>@<ip-addresss/hostname:port_number>/<database_name>'

# sqlAlchemy_Database_Url = f'postgresql://postgres:rootdb@localhost:5432/fastapi'
sqlAlchemy_Database_Url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# to connect with database postgresql instead of the normal connection with row-sql 
engine = create_engine(sqlAlchemy_Database_Url) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# to create the model [table] into database. 
Base = declarative_base()


# Dependency, to handle the session every time need to interact with database throughout a session,
#  then close that session, which more effeciant in performance.
def get_db():
    db = SessionLocal()
    # db = Session(local_session=SessionLocal())
    try:
        yield db
    finally:
        db.close()


# region handle the connection with datbase, either with row-sql

#  this is the way can use to connect with database using row-sql not ORM like with sqlAlchemy. 

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres',
#             password='rootdb',
#             cursor_factory=RealDictCursor
#         )

#         cusrsor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as error:
#         print('Database connection failed')
#         print('Error: ', error)
#         time.sleep(2)  # wait 2-seconds before return back to the loop .

# endregion
