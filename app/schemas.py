from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# the inner class config : used to convert the coming from database postgres sqlAlchemy_model
#   into a pydantic_model , to be able to convert it into dict and return it back to the client
#   in style of a dict.


# --------------------------------User----------------------------------------------

class UserCreated(BaseModel):
    # EmailStr : is an email with validation to make sure it's a valid email .
    email: EmailStr
    password: str


# user_response,

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True  # convert the response into a valid dict .


class UserOutRelation(BaseModel):
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True  # convert the response into a valid dict .


# ----------------------------------Post----------------------------------------

class BasePost(BaseModel):
    name: str
    content: str
    published: bool

    def __str__(self) -> str:
        return f'name : {self.name}, content: {self.content}, published: {self.published} '


class PostCreated(BasePost):
    pass


class PostUpdated(BasePost):
    pass


# response classes.

class PostOut(BasePost):
    id: int
    created_at: datetime
    user_id: int  # {ForeignKey}
    owner: UserOutRelation  # relation betwee tables User, Post.

    def __str__(self) -> str:
        return super().__str__() + f', id {self.id}, created_at: {self.created_at}, user_id: {self.user_id}'

    # append this config to treate the return response as a valid dict.
    class config:
        orm_mode = True


class PostVoteOutput(BaseModel):
    Post: PostOut
    votes: int

    def __str__(self) -> str:
        return super().__str__() + f', votes :{self.votes}'

    class config:
        orm_mode = True


# ------------------------------------Authentication---------------------------------


# either use this UserLogin , or using OAuth2PasswordRequestForm
# Authentication,
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# define a schema for the token where make sure the client must provide token , token_type.
class TokenOut(BaseModel):
    access_token: str
    token_type: str


# define a schema for the output when decoding the token,
# to return back what payload inside the token might be used.
class TokenData(BaseModel):
    id: Optional[int] = None

# ------------------------------------------Votes------------------------------------------


class VotesDirection(Enum):
    like = 1
    dislike = 0


class Vote(BaseModel):
    post_id: int
    dirc: VotesDirection = VotesDirection.like  # as default value .
