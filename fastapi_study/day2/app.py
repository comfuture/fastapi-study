from fastapi import FastAPI, Depends
from fastapi_study.day2.db import Session, use_db
from fastapi_study.day2.routes import user

def create_app():
    """creates a fastapi app"""
    fastapi_app = FastAPI()
    @fastapi_app.get('/')
    def index(db: Session = Depends(use_db)):
        """index page"""
        print(f'{db=}')
        return {}

    fastapi_app.include_router(user.router)

    return fastapi_app


# XXX
app = create_app()
