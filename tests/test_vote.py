
import pytest
from app import models


# TODO also can check about in case of the user who create the post try to make a vote, and disable
#       such a request, but our application dose not prevent a user from like/dislike it's post
#       this is not wron but this how the application worked . 


# -------------------------------fixture belong only for votes-------------------------

# such a vote would access directelly to the database where dose not have to work throughout a route, 
# use a session to handle the vote on a specific post directelly .
# note : you like the vote, when you create it in vote table .
@pytest.fixture()
def like_vote(session, test_posts, register):
    data = {
        "post_id": test_posts[0].id,
        "user_id": register[0]['id']
    }
    vote = models.Vote(**data)
    session.add(vote)
    session.commit()

# -------------------------------------------------------------------------------------

# TODO unauthorized user try to vote on a post /
def test_unauthorized_user_vote_on_post(client, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "dirc": 1
    }
    res = client.post('/votes/', json=data)

    assert res.status_code == 401  #unauthorized user. 



# TODO vote on a post dose not exist /
    
def test_vote_on_post_dose_not_exist(authorized_client_userone, test_posts):
    data = {
        "post_id": 100,
        "dirc": 1
    }
    res = authorized_client_userone.post('/votes/', json=data)
    res.status_code == 404 #post dose not exist 
    


# TODO vote on post with like '1' , which dose have like before /

def test_vote_like_on_post_dose_have_like_before(authorized_client_userone, like_vote, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "dirc": 1
    }
    res = authorized_client_userone.post('/votes/', json=data)

    assert res.status_code == 409 # conflict the vote dose exist before. 




# TODO vote on post with dislike '0' which dose have a like before/ dose no exist before. 

def test_vote_dislike_on_post_dose_not_exist_before(authorized_client_userone, register):
    data = {
        "post_id": 100,
        "dirc": 1
    }
    res = authorized_client_userone.post('/votes/', json=data)
    assert res.status_code == 404 # the vote dose not exist before .



# TODO vote on a post with like normally which dose not liked before and the post is exsit and the user
#       is login successfully.
    
def test_vote_on_post_normally(authorized_client_userone, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "dirc": 1
    }
    res = authorized_client_userone.post('/votes/', json = data) 
    assert res.status_code == 201 # create a new vote over post 0



# TODO vote on a post with dislike normally which do liked before and the post is exsit and the user
#       is login successfully.
    
def test_dislike_vote_liked_before(authorized_client_userone, like_vote, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "dirc": 0
    }
    res = authorized_client_userone.post('/votes/', json=data)

    assert res.status_code == 204 # vote dose not exist any more. 



    

