from typing import Dict, List, Literal
from fastapi.testclient import TestClient
import pytest
from app import schemas

# in this file will test all the posts routes :

# [imp] note : all the post routes required a token to execute the routes, so either make a fixture
#           which handle the login and get back a token before each route, or make your own token
#           into that fixture without calling the login route form OAuth module .


# now this test function depnding on the creation of a three posts as fixture before it's execution,
# where must found three posts in the table of posts.

# [imp] note : all the cases which based on the test_posts are interanlly called the register. 

# -------------------------------------get_posts----test--------------------------------------
def test_get_all_posts(authorized_client_userone, test_posts):
    res = authorized_client_userone.get('/posts/')

    def buildPost(post):
        return schemas.PostOut(**post)

    posts_map = map(buildPost, res.json())  # json is an iterator.
    posts_list = list(posts_map)

    print(posts_list)
    assert posts_list[0].id == test_posts[0].id
    assert posts_list[0].content == test_posts[0].content
    assert posts_list[0].name == test_posts[0].name
    assert res.status_code == 200


def test_unothorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    res.status_code == 401  # 401 for Unauthorized user.

# -------------------------------------get_one_posts----test--------------------------------------


def test_unathorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')  # /posts/1
    assert res.status_code == 401


def test_get_one_post_not_exist(client, test_posts):
    res = client.get('/posts/70000')
    res.status_code == 404  # 404 for not found


def test_get_one_post(authorized_client_userone, test_posts):
    res = authorized_client_userone.get(
        f'/posts/{test_posts[0].id}')  # /posts/1
    post = schemas.PostOut(**res.json())
    print(post)
    assert post.id == test_posts[0].id
    assert post.name == test_posts[0].name
    assert post.content == test_posts[0].content


# -------------------------------------create_post----test--------------------------------------

# TODO not_authorized,
def test_unathorized_create_post(client, register):
    res = client.post('/posts/', json={"name": "first_name",
                                       "content": "first_content", "published": True})
    res.status_code == 401  # unauthorized user.


# TODO postCreate shcmea not complete. inner situation in parametarized
def test_create_post_default_published_true(authorized_client_userone, register):
    res = authorized_client_userone.post(
        '/posts/', json={"name": "postName", "content": "postContent"})

    post = schemas.PostOut(**res.json())
    assert res.status_code == 201
    assert post.published == True
    assert post.name == "postName"
    assert post.content == "postContent"


# TODO finally create a post.
@pytest.mark.parametrize("name, content, published", [
    ('first_name', 'first_content', True),
    ('second_name', 'second_content', False),
    ('third_name', 'third_content', True),
    # ('third_name', 'third_content'), # check for the default value of published set to true.
])
def test_create_post(authorized_client_userone, register, name, content, published):
    res = authorized_client_userone.post(
        '/posts/', json={"name": name, "content": content, "published": published})

    post = schemas.PostOut(**res.json())

    assert res.status_code == 201  # create a new post.
    assert post.user_id == register[0]['id']
    assert post.name == name
    assert post.content == content
    assert post.published == published


# ---------------------------------Delete post----test----------------------------------------

# TODO unauthorized delete a post [without any login]

def test_unauthorized_delete_post_without_login_atAll(client, register, test_posts):
    # id of the first post, which belong to the first user register.
    res = client.delete(f'/posts/{test_posts[0].id}')

    res.status_code == 401 #unauthroized user. 


#TODO unauthorized delete a post, [login with different user, not the creator of the post]
def test_unathorized_delete_post_from_different_user(authorized_client_usertow, register, test_posts):
    # authorized_client_userone is the one who create test_posts[0], not user_two . 
    res = authorized_client_usertow.delete(f'/posts/{test_posts[0].id}')

    assert res.status_code == 403 #forbidden


# TODO delete a post with id dose not exist
def test_delete_post_with_id_not_exist(authorized_client_userone, test_posts):
    res = authorized_client_userone.delete('/posts/100')

    assert res.status_code == 404 #not found .



# TODO delete a post normally
def test_delete_post(authorized_client_userone, test_posts):

    res = authorized_client_userone.delete(f'/posts/{test_posts[0].id}')

    res_posts = authorized_client_userone.get('/posts/') # query all posts after delete one. 
    
    assert res.status_code == 204 # the item is delted successfully and not exist in database any more. 
    assert len(res_posts.json()) == (len(test_posts) - 1) # after delete one post. 
    

# ---------------------------------Update post----test----------------------------------------
    
# TODO unauthorized user, 
def test_unauthorized_update_post(client, test_posts): 
    data = {
        "name": "update name post",
        "content":"updated content post",
        "published": False
    }
    res = client.put(f'/posts/{test_posts[0].id}', json=data)
    
    assert res.status_code == 401



# TODO update post dose not eixist 
def test_update_post_not_exist(authorized_client_userone, test_posts): 
    data = {
        "name": "update name post",
        "content":"updated content post",
        "published": False
    }
    res = authorized_client_userone.put('/posts/100', json=data)
    
    assert res.status_code == 404



# TODO update post created by user_one from user_two, 
def test_update_post_cretae_by_another_user(authorized_client_usertow, test_posts): 
    data = {
        "name": "update name post",
        "content":"updated content post",
        "published": False
    }
    # try to update post created by the first user from here the second user. 
    res = authorized_client_usertow.put(f'/posts/{test_posts[0].id}', json=data)
    res.status_code == 403


# TODO update the post normally. 
def test_update_post(authorized_client_userone, test_posts):
    data = {
        "name": "update name post",
        "content":"updated content post",
        "published": False
    }
    res = authorized_client_userone.put(f'/posts/{test_posts[0].id}', json=data)
    updatePost = schemas.PostOut(**res.json())

    assert res.status_code == 200
    assert updatePost.name == data['name']
    assert updatePost.content ==  data['content']
    assert updatePost.published == data['published']