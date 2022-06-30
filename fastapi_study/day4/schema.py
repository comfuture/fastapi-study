from typing import Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field, SecretStr

kst = timezone(timedelta(hours=9))


def now(tz=kst):
    """returns current datetime"""
    return datetime.now(tz=tz)


class User(BaseModel):
    """base user scheme"""
    username: str = Field(title='유저명')
    password: SecretStr = Field(title='패스워드', exclude=True)

    class Config: # pylint: disable=missing-class-docstring
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "FooBar",
                "password": "hogehoge",
            }
        }
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class PostBase(BaseModel):
    """게시물 base"""
    title: str = Field(title='제목')
    content: Optional[str] = Field(title='내용')


class PostIn(PostBase):
    """게시물 (입력)"""
    username: str


class Post(PostBase):
    """게시물"""
    date_created: datetime = Field(title='작성일자', alias='dateCreated',
                                   default_factory=now)
    date_published: datetime = Field(title='게시일자', alias='datePublished')
    user: User = Field(title='작성자')
