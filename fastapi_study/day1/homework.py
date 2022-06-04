from typing import Optional
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel, validator

app = FastAPI()


async def use_queries(request: Request):
    """lookup queries in the request"""
    query = request.query_params
    return query


@app.get("/")
def has_many_queries(queries: dict = Depends(use_queries)):
    """
    ## 정해지지 않은 쿼리 파라메터를 모두 참조합니다.
    
    타잎을 지정할 수 없으므로 모두 string으로 처리됩니다.

    ```http
    GET /?name=value&age=value
    ```
    """
    return {
        'queries': queries
    }


class Queries(BaseModel):
    """쿼리 파라메터 인풋"""
    name: Optional[str] = None
    age: Optional[int] = 18

    @validator('age', pre=True)
    def validate_age(cls, value): # pylint: disable=no-self-argument
        """정수만 입력되도록 합니다."""
        try:
            return int(value)
        except ValueError:
            return 0 # 또는 예외를 발생시킴


@app.get("/with-models", response_model=Queries)
def with_models(queries: Queries = Depends(use_queries)):
    """
    ## 모델 정의와 함께 사용하기
    
    쿼리에서 모델에 정의한 속성들과 일치하는 파라메터들을 모아 모델 객체를 얻습니다. *정해지지 않은* 모든 쿼리를 얻겠다는 취지에서는 멀어졌지만,
    많은 수의 쿼리를 참조하기 위해 함수 정의부를 장황하게 나열하는 대신 json body 를 이용하는 것과 유사한 방법으로 모아 사용할 수 있습니다.

    request.query_params 의 각 값이 정의한 모델에 부합하지 않을 경우 `pydantic.error_wrappers.ValidationError`
    예외가 발생하여 의도치 않은 Internal Server Error 를 발생시키므로 모델에 적절한 방법으로 validator 를 설치해야 합니다.

    ```http
    GET /?name=value&age=value
    ```
    """
    return queries


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('fastapi_study.day1.homework:app', port=4000, reload=True)
