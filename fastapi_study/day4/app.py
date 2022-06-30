from fastapi import FastAPI

def create_app():
    """creates a fastapi app"""
    fastapi_app = FastAPI()
    @fastapi_app.get('/')
    def index():
        """index page"""
        return {'greeting': 'Hello!!!!'}

    return fastapi_app


# XXX
app = create_app()
