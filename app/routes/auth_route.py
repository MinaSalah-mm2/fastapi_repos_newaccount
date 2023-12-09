
from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schemas, models, utils, oauth

route = APIRouter(tags=['Authentication'])

# as use the oAuthRequestForm , must put the credential in the form-data of the body,
# also, can still working with normal schema to specify what the data coming would look like ?

# note : with OAuth2PasswordRequestForm there's no field called email it called username.



@route.post('/login', response_model=schemas.TokenOut)
def login(
    user_credential: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):

    user: models.User = db.query(models.User).filter(
        models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credential')

    # verify the user enter the correct password,
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credential')

    # create token & return .
    # in this dict, can add all info need to be attach to the token, like user_role, ...etc .
    token = oauth.createAccessToken(
        payload={'user_id': user.id})

    return {'access_token': token, 'token_type': 'bearer'}
