
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from . import database, models
from sqlalchemy.orm import Session
from fastapi import Depends
from .config import settings


# in this file, would handle all the O_auth security for the jwt and else.

# this mean, this oauth_schena would be used inside getCurrentUser as Depends, so
# make sure all pre-determined routes, would based on the login route, to make sure the
# client is Already login in and have a valid token and not expired one .
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# any random secret String,
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
# big the number just for testing purpose.
ACESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_minutes


def createAccessToken(payload: dict):
    toEncode = payload.copy()  # do not miss with original data.

    expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_TIME)
    toEncode.update({'exp': expire})

    encodedJWT = jwt.encode(toEncode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT


# scenario where a client want to create a post ?
#
# first, client login with username, password in the body.form-data,
#   result -> get a [token]
#
# second, client will add the token to the Authentication with request, to make post request .
#   in back-end ->
#   .. post() route, Depends on getCurrentUser(token),
#   .. token -> is a Depends(OAuth2PasswordBearer) where connect [ login with token get it ]
#   .. verify token is valid and not expired .
#
# finally if no exception being raised from verification, where the post function based on the
# function of verifying the token the post would occurred successfully.
#


def verifyAccessToken(token, credential_exception):
    # validate_token,
    # extract_payload, check payload is None, token is expired
    # return payload.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        if id is None:
            raise credential_exception

        # put id in schema of TokenData.
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credential_exception

    return token_data


# we would have a function called get_current_user(), where it would be used to ensure that
# for specific pre-determined end-points the client must be login and gain a valid and non-expired
# token to be able to process the route end-point, e.g. post() , ...etc
#
# so, this function would ne used as Depends() into other pre-determined routes.

# the second reason why we declare such a method here, is based on the verification method
# can return back the user, so we can now attach the returned user to any route use this function
# as a Depends for, and apply any logic related to the user. ` if you want `

# for example on the logic could be need when return a user from getCurrentUser, into a route,
# might check about the user role [normal, adman, ...etc] and based on the user role, give that
# user the ability to do some specific work the other might not to do .


def getCurrentUser(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(database.get_db)
) -> models.User:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f'could not validate the credential',
        headers={"www-Authenticate": "Bearer"}
    )

    tokenData = verifyAccessToken(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == tokenData.id).first()

    return user
