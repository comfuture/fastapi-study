from typing import Optional, Any, Union
from datetime import datetime
from fastapi import FastAPI, Header, Query, Depends
from pydantic import BaseModel, Field


class BlogEntryBase(BaseModel):
    title: str = Field(title="제목")
    body: str = Field(title="내용")


class BlogEntryPayload(BlogEntryBase):
    pass


class BlogEntry(BlogEntryBase):
    createdAt: datetime = Field(...)


class BlogEntryResponse(BaseModel):
    items: list[BlogEntry] = Field(title="블로그 항목들")


class JSONSchema4Object(BaseModel):
    """JSONSchema"""

    type: str
    title: Optional[str]
    description: Optional[str]
    properties: Optional[Any]  # XXX
    required: bool | str | list[bool | str]


def use_wants_schema(
    accept: Optional[str] = Header(
        None,
        alias="accept",
        title="Accept header",
        description="선호하는 응답 미디어 타잎.\n\n"
        "**available types:**\n"
        " - application/schema+json\n - application/json\n - \*/\*",
    ),
    alt: Optional[str] = Query(
        None,
        alias="type",
        description="Accept 헤더 대신 `type` 쿼리스트링에 선호하는 응답 미디어 타잎을 지정할 수 있습니다",
    ),
):
    """determine whether user wants schema instead of json"""
    print("accepts =", accept.split(";"))
    return any("schema+json" in t for t in accept.split(";")) or alt == "schema"


app = FastAPI()


def schema_vari(response_model: type) -> dict:
    return dict(
        response_model=response_model,
        responses={
            200: {
                "model": response_model | JSONSchema4Object,
                "content": {
                    "application/json": {"schema": response_model.schema()},
                    "application/schema+json": {"schema": JSONSchema4Object.schema()},
                },
            },
        },
    )


# @app.get(
#     "/",
#     response_model=BlogEntryResponse,
#     responses={
#         200: {
#             "model": BlogEntryResponse | JSONSchema4Object,
#             "content": {
#                 "application/json": {"schema": BlogEntryResponse.schema()},
#                 "application/schema+json": {"schema": JSONSchema4Object.schema()},
#             },
#         }
#     },
# )
@app.get("/", **schema_vari(BlogEntryResponse))
def index(client_wants_schema: bool = Depends(use_wants_schema)):
    if client_wants_schema:
        return BlogEntryPayload.schema()
    return BlogEntryResponse(
        items=[BlogEntry(title="hello", body="world", createdAt=datetime.now())]
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("day6.app", reload=True)
