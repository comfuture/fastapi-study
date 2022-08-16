from collections import Counter
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, validator


class Tag(BaseModel):
    """tag spec"""

    name: str = Field(title='tag name')
    value: str = Field(title='tag value')


class Resource(BaseModel):
    """resource spec"""
    _REQUIRED_KEYS = ['Name', 'Environment', 'Project']

    name: str = Field(title='resource name')
    tags: list[Tag] = Field(title='tags', default_factory=list,
                            contains={
                                'type': 'object',
                                'properties': {
                                    name: {'type': 'string'} for name in _REQUIRED_KEYS
                                },
                                **Tag.schema(),
                                'required': _REQUIRED_KEYS
                            },
                            description=f'it should have items that contains name={_REQUIRED_KEYS}',
                            uniquenessKey="#/name")

    @validator('tags')
    def validate_tags(cls, value): # pylint: disable=no-self-argument
        """validates whetere tags contains all required keys"""
        assert len((Counter(v.name for v in value) | Counter(_REQUIRED_KEYS)).elements()) == 3
        return value

app = FastAPI()


@app.get('/')
def list_resources():
    return Resource.schema()


@app.post('/')
def create_resource(item: Resource = Body(...)):
    ...


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)