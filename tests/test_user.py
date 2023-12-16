from app import schemas
import pytest
from jose import jwt
from app.config import settings

# all testing below look like the postman where client instance give me chance to send request
# with all other aspects of the request, header, token, body, ...etc

# note : in case of using the session as a Dependency with each test,
#  which mean can use it to create a query to interact with datbase.

# note : for most of routes testing required user_registeration, so instead of create_user with each
#        new test, have two soultions :
#   1, create a seprated @pytest.fixture which create a user before execute test for each each function.
#   2. use the scope of the fixture client/session , to be on the scope of the whole modeul not just scoe of the function,
#      where the fixture client/session would execute only once on the scope of the modeul [tests/test_user.py]
#      not before each function which is the default for the fixture before change the scope.

# conftest.py ->
# conftest.py, is a special file where can define all the fixture function, and by default pytest
# will allow any file within the test package to access this file without any import so, will have access
# to all the fixture without the need to import, in any file.


def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == 'hello world'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        '/users/', json={"email": "hello123@gmail.com", "password": "password1234"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


# test the login route, succesdfully login
def test_login_user(client, register):
    res = client.post(
        '/login', data={"username": register[0]['email'], "password": register[0]['password']})

    newToken = schemas.TokenOut(**res.json())
    payload = jwt.decode(newToken.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get('user_id')

    assert res.status_code == 200
    assert newToken.token_type == "bearer"
    assert id == register[0]['id']


# test the failure of the login .
@pytest.mark.parametrize("email, password, status_code", [
    ("hello123@gmail.com", "wrongPassword", 403),
    ("wongEmail@gmail.com", "password1234", 403),
    (None, "password1234", 422),
    ("hello123@gmail.com", None, 422),
    (None, None, 422)
])
def test_incorrect_login(client, register, email, password, status_code):
    res = client.post(
        '/login', data={"username": email, "password": password}
    )

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credential"


# TODO test get the user with specific id, 
# TODO test get the wrongUser/None based on the wrong id passed 
# TODO test can delete user based on specific id. 