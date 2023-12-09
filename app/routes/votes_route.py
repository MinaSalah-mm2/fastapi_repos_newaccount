from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from .. import database
from .. import oauth


route = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


# the main logic behind the vote table,
# once the vote [post_id, user_id] exist in the vote table, which mean , like such a post_id
#   with owner such a user_id, before.

# and once the search vote based on the post_id , not exist in the vote table, which mean
# this post with [post_id, user_id] is not voted (liked) before.

@route.post('/', status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(oauth.getCurrentUser)
):
    

    # first i make sure the user is log-in based on the Depends, but not sure if the post exist or not ?
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {vote.post_id} dose not exist.')

    # try to check if the vote is alredy exist before,
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == currentUser.id
    )

    found_vote = vote_query.first()

    if (vote.dirc == schemas.VotesDirection.like):  # 1
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"current user with this id: {currentUser.id} alredy voted on this post before. !")
        else:
            # creation of the votes mean the list of like from [post] reltively to user
            voteModel = models.Vote(
                user_id=currentUser.id, post_id=vote.post_id
            )
            db.add(voteModel)
            db.commit()
            return {'message': 'successfully added vote'}

    else:  # 0 => dislike
        if not found_vote:
            # rais excpetion, not existing.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"can not found the vote with id : {currentUser.id}")

        else:
            # delete such a vote, and this is the meaning of dislike,
            vote_query.delete(synchronize_session=False)
            db.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
