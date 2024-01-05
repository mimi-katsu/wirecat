from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Post(db.Model):
    post_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    author:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    html_content:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    summary:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    thumbnail:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    publish_date:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    tags:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    def __repr__(self):
        return f"{self.title}"

class User(db.Model):
    user_id:Mapped[int] = db.Column(db.Integer, primary_key=True)
    username:Mapped[str] = db.Column(db.String, unique=False, nullable=False)
    first_name:Mapped[str] = db.Column(db.String, unique=False, nullable=True)
    last_name:Mapped[str] = db.Column(db.String, unique=False, nullable=True)
    email:Mapped[str] = db.Column(db.String, unique=False, nullable=False)
    api_key:Mapped[str] = db.Column(db.String, unique=True, nullable=True)
    secret_key:Mapped[str] = db.Column(db.String, unique=False, nullable=True)
    password:Mapped[str] = db.Column(db.String, unique=False, nullable=False)
    def __repr__(self):
        return f"{self.username}"
    
class UserMeta(db.Model):
    user_id:Mapped[int] = db.Column(db.Integer, primary_key=True)
    username:Mapped[str] = db.Column(db.String, unique=True, nullable=False)
    def __repr__(self):
        return f"{self.username}"

class PostMeta(db.Model):
    post_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    views:Mapped[str] = db.Column(db.Integer, unique=False, nullable=False)
    updoots:Mapped[str] = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"{self.title}"

class Author(db.Model):
    user_id:Mapped[str] = mapped_column(String, primary_key=True)
    username:Mapped[str] = mapped_column(String, unique=True, nullable=False)
    photo_path:Mapped[str] = mapped_column(String, unique=True, nullable=True)
    first_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    last_name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    experience:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    about:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    posts:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    def __repr__(self):
        return f'{self.username}'