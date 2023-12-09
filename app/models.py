
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

# note: when try to make some modification like add new column or update existing one, ...etc,
#     have to delete the post manually using pgAdmain, or using a tool for migration database
#     like the most famous one Alembic .

# note : let's assume you want in a single table contains two or more column make a unique row
#        based on tow or more columns, where can not insert a new tow contains values which
#        alredy exist before, have two soultion
#
#        1. using the composite_key and make those two or more columns key inside that composite key,
#        2. make a unique index for thoes tow or more columns need to make theme un-rebetable.
#
#    e.g. => for a social media app, we have like's sub-sysmte where the client must like the
#            post only once , so can make the post_id and the owner_id of post either a composite key,
#            or make a unique index for both columns ...


# note_impo =>
#
# -- # calculate number of posts for each user.
# 
# select users.id, COUNT(posts.id) from users 
#      left join posts on posts.user_id = users.id group by users.id;
# 
# 
# --  # calculate number of votes for each posts. 
# 
# select posts.id as post_id, COUNT(votes.post_id) as votes from posts 
#      left join votes on posts.id = votes.post_id group by posts.id;
# 
# 


# note: alembic. 
#   is a migration tools to handle the migration for the database tables. 
#   as the git for handling the software also alembic has many features as git handle the database, 
#   and could also roolback to specific point at the database tables, exactelly like git .
# 
# how to interact with alembic ? 
#  1. create an alembic directory to keep track any change just like git , 
#       $ alembic init `directory_name`
# 
#  2. as alembic working with sqlAchemy models, we need to make sure it have access to Base object,
#     in the 'model' class 
#  
#  3. to create a new version with alembic to handle some things inside this version like create a new tables , ...etc 
#     $ alembic revision -m "create new posts table"  , just lije the commit with git . 
#  
#  4. to apply this change for a specific revision version ...
#     $ alembic upgrade 'revision_version_number/ID'
# 
#  note : to show all the previouse upgrade based on revsions being created. 
#       $ alembic history 
# 
# 
#  note : alembic is a smart tool where it can autoGenerate the tables/Columns in case of required 
#         based on the models being built before by sqlAlchemy only if such a model existing, 
#         with command line --autoGenerate will chekc about the difference and the table/columns
#         being generated before by normal sqlAlchemy and not generated yet, and it will built such 
#         missing tables/columns 
# 
#         . it's not nesseccary to have a sqlAlchemy to work with alembic ...
# 
#   
#  note : never ever with alembic revision implement the upgrade without the downgrade . 
# 
# 



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    # relation between tow tables without sqlQuery, append the user table on this post table to output as json .
    owner = relationship('User')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))



class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
