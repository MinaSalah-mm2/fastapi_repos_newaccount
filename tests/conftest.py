
import pytest
from typing import List, Dict
from app.main import app
from fastapi.testclient import TestClient
from app import models
from app.database import get_db
from sqlalchemy import create_engine
# define table mapping, instead of baseModel
from sqlalchemy.ext.declarative import declarative_base
# to make read/write opeartions with postgres.
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app import schemas
from app import oauth

# note : this file conftest is accessiable from all the files within the test package, there's no
#        need to import this file form any other files.


# in this test_user file, will test every thing related to the user  in the API, e.g.
# CRUD for user, autherization for user and return back the token , ..etc/

# notes all the options in the command with pytest :
# ---------------------------------------------------
# -v  => to display the test passed/failure with in in string not just a dot .
# -s  => to dispaly a string in case of the pytest function print some string,
# --disable-warnings => display the warnings,
# -x  => this option simulate as a flag in case of have many pytest function and once hit the first function to failed pytest will stop
#        to try to fix this issus in this function first ...

# with testing should not use the same database used in the production, so must create a new
# database only for testing and use the fixture to drop then create all the tables before any
# CRUD processes, and must hanle the database coming from the app which existing in the main
# file to change the dependecy for each route in case of the testing to the new database_tables.


# the only different in the url the database name end with _test.
sqlAlchemy_Database_Url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# to connect with database postgresql instead of the normal connection with row-sql
engine = create_engine(sqlAlchemy_Database_Url)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# to create the model [table] into database.
Base = declarative_base()


@pytest.fixture
def session() -> sessionmaker:
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()  # give me a session to work with database.
    try:
        yield db
    finally:
        db.close()


# a function to execute before each test function.
@pytest.fixture
def client(session) -> TestClient:
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # switch to the Dependency of each route to the tables of the new database fastapi_texst/
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


# create_User, Register, sanjev call it 'test_user'
@pytest.fixture
def register(client) -> List[Dict]:
    res1 = client.post(
        '/users/', json={"email": "hello123@gmail.com", "password": "password1234"}
    )

    res2 = client.post(
        '/users/', json={"email": "hello123321@gmail.com", "password": "password12344321"}
    )

    assert res1.status_code == 201
    assert res2.status_code == 201

    userOut1 = schemas.UserOut(**res1.json())
    userOut2 = schemas.UserOut(**res2.json())

    newUser1 = dict(**userOut1.__dict__)
    newUser2 = dict(**userOut2.__dict__)

    newUser1["password"] = "password1234"
    newUser2["password"] = "password12344321"

    userLists = []
    userLists.append(newUser1)
    userLists.append(newUser2)
    return userLists


# fixture, to simulate and fake the creation of a jwt token, instead of login before each route in test_post.

@pytest.fixture
def token_userone(register) -> str:
    return oauth.createAccessToken(
        payload={'user_id': register[0]['id']}
    )

@pytest.fixture
def token_usertwo(register) -> str:
    return oauth.createAccessToken(
        payload={'user_id': register[1]['id']}
    )



# this is also a client with appended token as authorized client.
@pytest.fixture
def authorized_client_userone(client, token_userone) -> TestClient:
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_userone}"
    }

    return client

# this is also a client with appended token as authorized client.
@pytest.fixture
def authorized_client_usertow(client, token_usertwo) -> TestClient:
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_usertwo}"
    }

    return client


# to check getAllPosts, update, delete, ...etc for posts, have to create some posts without using
#   the route with authorization_client. ... can do that with session direct work with database
#   using TestSessionlocal.


def create_post(post):
    return models.Post(**post)


#  this fixture for creating some posts, without testing any route to be use with other posts route,
# simulate there's posts in the database post table .
@pytest.fixture
def test_posts(session, register):
    # posts :
    posts_data = [
        {
            "name": "mena salah",
            "content": "Alorithm and the important of using the math for the algorithms .",
            "published": True,
            "user_id": register[0]['id']
        },
        {
            "name": "scarlet johanson",
            "content": "marvel company make the stories into reality with dums movies.",
            "published": True,
            "user_id": register[0]['id']
        },
        {
            "name": "Albachino",
            "content": "the God Father was a movie wearing a worlf clothes.",
            "published": True,
            "user_id": register[0]['id']
        },
        {
            "name": "post_usertwo",
            "content": "content user two ",
            "published": True,
            "user_id": register[1]['id']
        },
        {
            "name": "post_usertwo second post name ",
            "content": "post_usertwo second post content,",
            "published": True,
            "user_id": register[1]['id']
        }
    ]
    posts_map = map(create_post, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()
    allPosts = session.query(models.Post).all()
    return allPosts
