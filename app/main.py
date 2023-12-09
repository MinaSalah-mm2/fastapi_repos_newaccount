
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routes import auth_route, post_route, user_route, votes_route
from .config import settings


# TODO note : upgrade the sqlAlchemy package verions to check if the wrong return from the method
# TODO      which return non instead of actual sqlAlchemy Model . is that would make different or not ? 


# region main_docsven

# to start switch the terminal command to work with venv & start uvicorn server :
#   1. switch the termianl => source venv/bin/actived
#   2. uvicorn app.main:app --reload

# note : the app.get -> is the path which working with pyhton-decorator.
# note : route == path
# note : FastApi automatically conver the the python dictionary into a json object.
# note : to run server with reloading, ~ uvicorn main:app --reload

# how to extract the data out of the coming body with post request ?
#   . using Body(...), from FastApi, to convert into dic and use it .

# how to enforce the client to send exactelly what you expected in the payload `schema` ?
#   . we can use [pydantic] lib, where FastApi can use this lib.
#   . so, with pydantic can validate the coming payload, and throw error if not match
#      also, do no have to use the Body(...) from FastApi to convert the coming payload into actual dic,
#      pydantic will take care of that .

# how to make a variable optional in python ?
#  rating: Optional[int] = None

# how to handle the error for the client who write website/mobile app ?
#   either using the Respoonse as a parameter in the route with status code.
#   or fire an HttpException which contains all the details from FastApi . `which is better`.

# to change the status_code return back with any route in case of it's not error ?
#   can attach the status_code in the route function itself and FastApi would handle the rest.

# when delete a post with FastApi, must not return a value or will make an error in the server.
#  must only return a response or exception.

# note : with FastApi there's automation docs do not have to write any docs,
#           can access those docs =>  [http://127.0.0.1:8000/docs]

# to create python package, python force you to create a folder and add a file into that folder ,
#  calle it [__init__.dart ] , now python treate that folder as a package .

# note : in python programming language : where have a function with paramter **param =>
#           this is mean take parameter like param in other language and return it in style of dict.
#           , also can do the vise-versa where take a dict and subtracing the values of it /


# note : what is the meaning of sql-injection =>
#   .  assume the client want to post into database, and send in one of the parameter data like [INSERT INTO ....]
#       so, in case of not using the way to execute variables %s , would cause a crach called sql-injection.

# note : instead of using sql-query, can using the ORM [object relational model] to descripe what
#           operation need, where this techinque internally used the sql and psycopg2 and read and write with postgres sql database.

# note : the most popular technique used for handle the read/write with postgres sql database is  :
#           `sqlAlchemy`

# SqlAlchemy => is a stand alone library and has no associalted with FastApi, it can be used with
#                  any other python frameworks or any python based application.

# note : Also SqlAlchemy can execute the query simultensouly, as more than one query at a time,
#           which is the opposite of the row-query.

# note: SqlAlchemy itself do not know how to connect with datbase and make operations, so need to use a driver
#           to handle the connections/operations which is the [psycopg2] package.

# note: the sqlAlchemsdssssscreate the query for you. instead of explicitly write those queries,


# note: what are the difference between [ schema/pydantic_model , sqlAlchemy_model ] ?
#       . schema/pydantic_model define the structure of the request & response .
#           ..this ensure that when user want to create a post, the request must contains post_name,
#               post_content, post_published .
#           .. summery the schema/pydantic_model make sure validate the coming request to match a specific schema
#           .. Also schema/pydantic_model can handle the response back, can specifiy specific attripute to return back to the user.
#
#       . sqlAlchemy_model => used to defining the table within the postgres Database,
#           .. also used to apply the CRUD operations .


# Authentication => (who are you), there's tow main ways : 
#   1. keep tracking about the user, where can not make any operation CRUD, without user-login .
#   2. using the JWT Token, where it's statless, there's no tracking for the user login, just using the token concept .
#
#
# . JWT_token => is a string consist of [header + payload + hashing]. 
# . signature -> is [Header + payload]
# . how to create JWT_Token => [Header + Signiture + payload] + secret.  
# . secret => is a secret key existing only on the server api , no one know about it .
#      use this scret to create toke, and for validation that the coming token is the real token 
#      being sent to the client ... by combing again the coming [header + signature, payload] + secret
#      if match the coming token then it's a valid token. 
#
# Authorization => (what can access), 
# 

# note : when a user make a registeration for the first time and provide a password, api will
#        hash this password and store it in the database, but when user try to log in have to 
#        send the password again, then api will take the coming password and query the hashed_password
#        from the database, then hash the coming password again to able to compare the coming hashed password
#        from the client with one coming form the database being hashed in the registration time  .
# 
#        then the Api can generate the token with JWT based on the coming hashed password and other info .
#        


# note: about the join tables together ? 
#    well, to join posts table specified columns and specifide columns from the user table, 
#    either try it with the query from postgres database, or just write a function which will 
#    query all the posts and users in both tables, and apply some logic over this function to count 
#    number of posts per each user. ? but with this approach of counting after quert every things 
#    that would be a little costlly, becuase, assume there's multiply posts and multiply users to thounds or even millions 
#    that query would be so much bad !



# note TODO the documentation about alembic in the model class. 



# note : CORS problem -> where while using the postman all the request fired being occurred 
#         on this localhost/device which mean working on the same domain but in case of trying to 
#         access this api which on the localhost from another domain such as `goodle` will fire 
#         such a problem CORS, which mean => [Cross Origin Resources Sharing], 
#         which allow you to make a request from one browser on one domain to a server on a 
#         different domains  e.g. {google_domain -> localhost_domain}...
# 
#         . by default our api will only allow web browser to running on the same domain 
#           as our server to make a requests to it. 
# 
#         . soultion => use the CORSMiddleWare. to solve the domain problem . 





# endregion

print(settings.database_username)
  

# create all the models [database_tables] using sqlAlchemy with this line  =>
# note : you do not need such a line of code as the alembic package handle the creation of 
#           all tables/columns needed ...

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# to solve the problem of the CORS, using the CORSMiddleWare. 

# note : if you specifiy a * instead of all those items in the list. as like open this api for any website to use it . 
origins = ["*"]

# explaning the middleWare problem sections : 
# allow_origins -> all the allow domains to talk with this api domain. like origins list. 
# allow_credentials -> allow the credentials like the email and password and based on that can re-send back a jwt token .
# allow_methods -> not only allow specific domain, can also allow specific http methods e.g. [post, get] only for example. 
# allow_header -> allow the client can send a specific headers. 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# declare a route for handling the course with the website, 
@app.get('/')
def my_root():
    return {"output" : "Hello world"}

# including the routes : 
app.include_router(post_route.route)
app.include_router(user_route.route)
app.include_router(auth_route.route)
app.include_router(votes_route.route)

