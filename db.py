from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref
from sqlalchemy import Integer, String, Boolean, ForeignKey

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Post(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id:Mapped[str] = mapped_column(String, unique=True, nullable=False) 
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    slug:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    html_content:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    summary:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    thumbnail:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    publish_date:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    published:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    featured:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    author = relationship('User', backref='post')

    def __repr__(self):
        return f"{self.slug}"

class PostMeta(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id:Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    views:Mapped[str] = mapped_column(Integer, unique=False, nullable=False, default=0)
    upvotes:Mapped[str] = mapped_column(Integer, unique=False, nullable=False, default=0)
    favorites:Mapped[str] = mapped_column(Integer, unique=False, nullable=False, default=0)
    tags:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    post = relationship('Post', backref=backref('meta', uselist=False))

    def __repr__(self):
        return f"{self.title}"

class User(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    verified:Mapped[bool] = mapped_column(Boolean, unique=False, default=False, nullable=False)
    creation_date:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    username:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    last_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    email:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    # Permissions types
    #   superadmin - Modify admin accounts, create authors
    #   admin - Moderate Content, approve posts, ban users, modify user accounts.
    #   author - Create posts
    #   user - View posts, make comments, like, share, etc
    perm:Mapped[str] = mapped_column(String, unique=False, nullable=False, default='user')
    def __repr__(self):
        return f"{self.username}"
    
class UserMeta(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    favorites:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    upvotes:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    views:Mapped[str] = mapped_column(Integer, unique=False, nullable=True, default=0)
    user = relationship('User', backref=backref('meta', uselist=False))

    def __repr__(self):
        return f"{self.user_id}"

class Profile(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    gender:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    photo_path:Mapped[str] = mapped_column(String, unique=True, nullable=True)
    first_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    last_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    dob:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    experience:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    about:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    posts:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    user = relationship('User', backref=backref('profile', uselist=False))
    def __repr__(self):
        return f'{self.user_id}'

class ApiKeys(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), unique = True, nullable=True)
    key:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expires:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    user = relationship('User', backref=backref('keys', uselist=False))
    def __repr__(self):
        return f'{self.user_id}'

class Announcement(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    post_date:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    content:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    author:Mapped[str] = mapped_column(String, unique=False, nullable=False)
    def __repr__(self):
        return f'{self.content} - {self.author}'