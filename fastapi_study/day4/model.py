from datetime import datetime, timedelta, timezone
from fastapi_study.day4.db import (
    BaseModel, Column, Integer, Unicode, UnicodeText, String,
    DateTime, relationship, ForeignKey)

kst = timezone(timedelta(hours=9))


def now(tz=kst):
    """returns current datetime"""
    return datetime.now(tz=tz)


class User(BaseModel):
    """user model"""
    id = Column(Integer, primary_key=True)
    username = Column(Unicode, nullable=False)
    password_hash = Column(String, nullable=False)

    posts = relationship('Post', back_populates='user',
        order_by='desc(Post.date_created)', lazy='select')

    __tablename__ = 'user'

    def __repr__(self):
        return f'<User {self.username}>'


class Post(BaseModel):
    """post model"""
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    content = Column(UnicodeText)
    date_created = Column(DateTime, default=now)
    date_published = Column(DateTime)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("Parent", back_populates='posts', lazy='joined')

    __tablename__ = 'post'

    def __repr__(self):
        return f'<Post title={self.title}>'
