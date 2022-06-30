from typing import Optional, Any
from datetime import datetime
from fastapi import FastAPI, Depends, Header, Query
from pydantic import BaseModel, Field

app = FastAPI()


class PostBase(BaseModel):
    """게시물 base"""
    title: str = Field(title='제목')


class PostListItem(PostBase):
    """게시물 목록 아이템"""
    created_at: datetime = Field(title='작성일시', alias='createdAt',
                                 default_factory=datetime.now)


class PostPayload(PostBase):
    """게시물 유저 데이터"""
    content: str = Field(title='내용')


class PostResponse(PostBase):
    """게시물 응답 데이터"""
    id: Optional[int] = Field(title='ID')
    created_at: datetime = Field(title='작성일시', alias='createdAt')


class JSONSchema4Object(BaseModel):
    """JSONSchema"""
    title: str
    type: str
    description: Optional[str]
    properties: Optional[Any] # XXX
    required: str | list


def use_wants_schema(accept: Optional[str] = Header(None, alias='accept'),
                     alt: Optional[str] = Query(None, alias='type')):
    """determine whether user wants schema instead of json"""
    print('accepts =', accept.split(';'))
    return any('schema+json' in t for t in accept.split(';')) or alt == 'schema'


@app.get('/', response_model=list[PostListItem] | JSONSchema4Object,
         responses={
            200: {
                "content": {
                    "application/json": {},
                    "application/schema+json": {
                        "example": PostPayload.schema()
                    },
                },
            }
         })
async def list_posts(client_wants_schema: bool = Depends(use_wants_schema)):
    """PostListItem 의 목록 또는 PostPayload의 jsonSchema를 보여줍니다.
    accept 헤더에 `application/schema+json` 을 명시하거나 `?type=schema` 쿼리스트링을 전달하여
    컬렉션의 스키마를 얻을 수 있습니다.
    """
    if client_wants_schema:
        return PostPayload.schema()
    return [PostListItem(title='hello')]

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('day5.app', reload=True)
