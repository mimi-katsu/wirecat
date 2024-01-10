from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, joinedload
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String, unique=False, nullable=True)
class Post(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    title:Mapped[str] = mapped_column(String, unique=False, nullable=True)
    content:Mapped[str] = mapped_column(String, unique=False, nullable=True)
