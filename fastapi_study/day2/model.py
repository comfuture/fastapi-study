from fastapi_study.day2.db import BaseModel, Column, Integer, Unicode


class User(BaseModel):
    """user model"""
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    age = Column(Integer, default=0)

    __tablename__ = 'user'

    def __repr__(self):
        return f'<User name={self.name}>'
