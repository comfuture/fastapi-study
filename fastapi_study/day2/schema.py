from typing import Optional
from pydantic import BaseModel, NonNegativeInt, Field


class UserBase(BaseModel):
    """base user scheme"""
    name: Optional[str] = Field(title='이름')
    age: Optional[NonNegativeInt] = Field(title='나이', default_factory=int)

    class Config:
        schema_extra = {
            "example": {
                "name": "FooBar",
                "age": 18,
            }
        }
