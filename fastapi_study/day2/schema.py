from typing import Optional
from pydantic import BaseModel, NonNegativeInt, Field


class UserBase(BaseModel):
    """base user scheme"""
    name: Optional[str] = Field(title='이름')
    age: Optional[NonNegativeInt] = Field(title='나이', default_factory=int)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "FooBar",
                "age": 18,
            }
        }


class UserEntry(UserBase):
    """user database entry"""
    id: int = Field(title='ID')


class UserEntryList(BaseModel):
    items: list[UserEntry]
