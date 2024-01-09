from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, joinedload
from sqlalchemy import Integer, String, Boolean, JSON, DateTime, ForeignKey
from datetime import datetime
import uuid
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Post(db.Model):
    #delete this one
    post_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    # add these
    # id:Mapped[int] = mapped_column(Integer, primary_key=True)
    # post_id:Mapped[str] = mapped_column(String, unique=True, nullable=False, default=uuid.uuid4())
    slug:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    author:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    html_content:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    summary:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    thumbnail:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    publish_date:Mapped[str] = mapped_column(String, unique=False, nullable=False, default=datetime.now())
    #delete tags
    tags:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    # meta = relationship('PostMeta', back_populates='post', uselist=False)
    # featured:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    def __repr__(self):
        return f"{self.title}"
    # def __repr__(self):
    #     return f"{self.slug}"

class PostMeta(db.Model):
    post_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    views:Mapped[str] = db.Column(db.Integer, unique=False, nullable=False)
    updoots:Mapped[str] = db.Column(db.Integer, unique=False, nullable=False)
    # id:Mapped[int] = mapped_column(Integer, primary_key=True)
    # post_id:Mapped[int] = mapped_column(Integer, foreign_keys='post.id', nullable=False, default=uuid.uuid4())
    # views:Mapped[str] = mapped_column(Integer, unique=False, nullable=False, default=0)
    # upvotes:Mapped[str] = mapped_column(Integer, unique=False, nullable=False, default=0)
    # downvotes:Mapped[str] = mapped_column(Integer, unique=False, nullable=False, default=0)
    # favorites:Mapped[str] = mapped_column(Integer, unique=False, nullable=False, default=0)
    # tags:Mapped[str] = mapped_column(String, unique=False, nullable=True, default="")
    # post = relationship('Post', back_populates='meta')
    def __repr__(self):
        return f"{self.title}"

class User(db.Model):
    # remove this one
    user_id:Mapped[int] = db.Column(db.Integer, primary_key=True)
    # add these
    # id:Mapped[int] = mapped_column(Integer, primary_key=True)
    # user_id:Mapped[str] = mapped_column(String, unique=True, nullable=False, default=uuid.uuid4())
    # verfified:Mapped[bool] = mapped_column(Boolean, unique=False, default=False, nullable=False)
    # creation_date:Mapped[str] = mapped_column(Boolean, unique=False, default=False, nullable=False)
    # meta = relationship('UserMeta', back_populates='user', uselist=False)
    username:Mapped[str] = db.Column(db.String, unique=True, nullable=False)
    first_name:Mapped[str] = db.Column(db.String, unique=False, nullable=True)
    last_name:Mapped[str] = db.Column(db.String, unique=False, nullable=True)
    email:Mapped[str] = db.Column(db.String, unique=True, nullable=False)
    # Permissions types
    #   SuperAdmin - Modify admin accounts, create authors
    #   Admin - Moderate Content, approve posts, ban users, modify user accounts.
    #   Author - Create posts
    #   User - View posts, make comments, like, share, etc
    # perm:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    # TODO: remove keys
    api_key:Mapped[str] = db.Column(db.String, unique=True, nullable=True)
    secret_key:Mapped[str] = db.Column(db.String, unique=False, nullable=True)
    password:Mapped[str] = db.Column(db.String, unique=False, nullable=False)
    # keys = relationship('ApiKeys', back_populates='user_id', uselist=False)
    def __repr__(self):
        return f"{self.username}"
    
# class UserMeta(db.Model):
#     id:Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id:Mapped[int] = mapped_column(Integer, foreign_keys='user.id', nullable=False)
#     user = relationship('User', back_populates('meta'))
#     def __repr__(self):
#         return f"{self.username}"

class Author(db.Model):
    #remove this one
    user_id:Mapped[str] = mapped_column(String, primary_key=True)
    # add these
    # id:Mapped[int] = mapped_column(Integer, primary_key=True)
    # user_id:Mapped[str] = mapped_column(String, foreign_keys='user.id', nullable=False)
    # remove this one
    username:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    # gender:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    photo_path:Mapped[str] = mapped_column(String, unique=True, nullable=True)
    first_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    last_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    dob:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    experience:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    about:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    posts:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    # user = relationship('User', back_populates='author')
    def __repr__(self):
        return f'{self.username}'

# class ApiKeys(db.Model):
#     id:Mapped[int] = mapped_column(Integer, primary_key=True)
#     key:Mapped[str] = mapped_column(String, unique=True, nullable=False)
#     expires:Mapped[str] = mapped_column(String, unique=True, nullable=False)
#     user = relationship('User', back_populates='keys')
#     user:Mapped[str] = mapped_column(integer, foreign_keys='user.id', nullable=False)

# post_with_metadata = Post.query.options(joinedload(Post.meta)).filter_by(post_id='some id').first()