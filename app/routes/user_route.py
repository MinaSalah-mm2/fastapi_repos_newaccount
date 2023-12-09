
from fastapi import status, HTTPException, Depends, APIRouter, Response
# make the connection and execute operations with postgreSql database .
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. import database
from .. import oauth

route = APIRouter(
    prefix='/users',
    tags=['Users']  # didive the docs into ground, one called Users
)


# region routes_user

# this is the same as Register.
@route.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    payload: schemas.UserCreated,
    db: Session = Depends(database.get_db)
):

    hashed_password = utils.hash(payload.password)
    payload.password = hashed_password

    # convert into dict, and unpack .
    user = models.User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@route.get('/{id}', response_model=schemas.UserOut)
def get_user(
    id: int, db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser)
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id : {id}, it not exisit.')

    return user


# unRegister
@route.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser) # depends on user is already login .
):
    user_query = db.query(models.User).filter(models.User.id == currentUser.id)

    if (user_query.first() == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id : {id} was not found !')
    
    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# endregion
