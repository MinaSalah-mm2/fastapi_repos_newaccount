from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
# make the connection and execute operations with postgreSql database .
from sqlalchemy.orm import Session
# import this to use count function in query .
from sqlalchemy import func
from .. import models, schemas
from .. import database
from .. import oauth

# query with sqlAlchemy is so simply, as => limit, offset, ....any many other based
# on the logic you want to apply it, e.g. search, ...etc
#

route = APIRouter(
    prefix='/posts',
    tags=['Posts']  # didive the docs into ground, one called Posts
)

# region routes_post


@route.get('/', response_model=List[schemas.PostOut])  # List from typing
def get_posts(
    db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser),
    limit: Optional[int] = None,
    page: Optional[int] = None
):
    # to perfoem the pagination, need to calculate the current page with limit to specify the offset.

    if (limit != None and limit < 0):
        limit = 0

    if (page != None and page < 1):
        page = 1

    skip: int = 0

    if (page and limit) != None:
        skip = (page * limit) - limit

    print(skip)

    posts = db.query(models.Post).limit(limit).offset(skip).all()
    return posts


@route.get('/posts_votes')
def get_posts_Votes(
    db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser),
    limit: Optional[int] = None,
    page: Optional[int] = None
):
    if (limit != None and limit < 0):
        limit = 0

    if (page != None and page < 1):
        page = 1

    skip: int = 0

    if (page and limit) != None:
        skip = (page * limit) - limit

    print(skip)

    # the query now is a joining between the posts and votes tables, for a pre-defined columns.
    # explaning this query ->
    # query -> query take more than one parameter where could take, (models_name,
    #           count_func)
    # join -> take two parameter, (join_table, on_constraints),   note : join() by default LEFT INNER JOIN
    # lable -> change the name of the votes only in the display as json it's like [as] in query
    # group_by -> group the post.id rows where group the similiar row if exist in one row [in this query there's not similiar posts]

    posts_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).limit(limit).offset(skip).all()
    # print(posts_votes)  # print the query itself.
    return posts_votes


@route.get('/{id}', response_model=schemas.PostOut)
def get_post(
    id: int, db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser)
):

    db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if (not post):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found!')

    # this user not the creator of this post.
    if (post.user_id != currentUser.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='user with such credential not allowed to access this content!')

    return post



@route.get('/posts_votes/{id}', response_model=schemas.PostVoteOutput)
def get_post_Votes(
    id: int, db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser)
):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    

    if (not post):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found!')


    print(post.__str__())

    return post



@route.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(
    payload: schemas.PostCreated,
    db: Session = Depends(database.get_db),
    # there's a token with the coming request.
    currentUser: models.User = Depends(oauth.getCurrentUser)
):

    # instead of write all that failed can uase the unpacet dict, =>
    # (name=payload.name, content=payload.content,published=payload.published)  into   **payload.dict()

    new_post = models.Post(user_id=currentUser.id, **payload.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # to returning the new_post for client .

    if (not new_post):
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='failed to add a new post !')

    return new_post


@route.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser)
):
    # return actual query .
    query_post = db.query(models.Post).filter(models.Post.id == id)

    post = query_post.first()

    if (post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'the post with id : {id} was not found !')

    if (post.user_id != currentUser.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='user with this credential not allowed to delete this content')

    query_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@route.put('/{id}', response_model=schemas.PostOut)
def update_post(
    id: int, payload: schemas.PostUpdated, db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser)
):
    query_post = db.query(models.Post).filter(models.Post.id == id)

    post = query_post.first()

    if (post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not exist !')

    if (post.user_id != currentUser.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='user with this credential not allowed to update this content')

    query_post.update(payload.model_dump(), synchronize_session=False)
    db.commit()

    return query_post.first()

# endregion


# region healping funtionalities
# fake simulation for database in style of a list :
my_posts = [
    {
        'id': 1,
        'title': 'the first post title',
        'content': 'the fisrt post content',
    },
    {
        'id': 2,
        'title': 'the second post title',
        'content': 'the second post content',
    },
    {
        'id': 3,
        'title': 'the third post title',
        'content': 'the third post content',
    },
    {
        'id': 4,
        'title': 'the fourth post title',
        'content': 'the fourth post content',
    },
    {
        'id': 5,
        'title': 'the fifth post title',
        'content': 'the fifth post content',
    },
]


def findPost(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post


def findIndex(id: int):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i
    return -1

# endregion

# region (main-region) routes for row-sql with sql query and postgresql


# @route.get('/')
# def root():
#     return {'message': 'Hello world with --reload'}


# @route.get('/posts')
# def get_posts():
#     cusrsor.execute("""SELECT * FROM posts;""")
#     posts = cusrsor.fetchall()
#     return {'posts': posts}  # fastApi by default will serialized into json .


# add response as a parameter in case of want to change the status_code with commented way.
# @route.get('/posts/{id}')
# def get_post(id: int, response: Response):
#     cusrsor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
#     post = cusrsor.fetchone()

#     if (not post):
#         raise HTTPException(status.HTTP_404_NOT_FOUND,
#                             detail=f'post with id: {id} was not found!')
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message' : f'post with id: {id} was not found!'}
#     return {'post': post}


# region old way to serialize the coming json into dictionary python object
# @route.post('/posts')
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {'the-payload': f'payload => title : {payload["title"]}, content : {payload["content"]}'}
# endregion


# @route.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_post(payload: Post):
#     cusrsor.execute(
#         """ Insert Into posts (name, content, published) Values (%s, %s, %s) returning *""",
#         (payload.name, payload.content, payload.published))

#     newPost = cusrsor.fetchone()
#     conn.commit()

#     if (not newPost):
#         raise HTTPException(
#             status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='failed to add a new post !')

#     return {'data', newPost}


# delete functions .

# @route.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cusrsor.execute(
#         """ DELETE FROM posts WHERE id = %s returning *""", (str(id),))
#     delete_post = cusrsor.fetchone()
#     conn.commit()

#     if (not delete_post):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'the post with id : {id} was not found !')

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# update [put, patch]

# @route.put('/posts/put/{id}')
# def update_post(id: int, post: Post):
#     cusrsor.execute(
#         """ Update posts Set name = %s, content = %s, published = %s where id = %s returning *""",
#         (post.name, post.content, post.published, str(id),))

#     updatedPost = cusrsor.fetchone()
#     conn.commit()

#     if (not updatedPost):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'post with id: {id} was not exist !')

#     return {'data': updatedPost}


# endregion
