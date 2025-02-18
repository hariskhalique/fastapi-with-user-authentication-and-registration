import uvicorn
from fastapi import FastAPI
from app.config.config import app_config
from app.app_module import app_module

def create_app() -> FastAPI:
    """ Create FastAPI app and register modules """
    app = FastAPI(debug=app_config.DEBUG)
    app_module(app)  # Register all application components
    return app

app = create_app()  # Initialize application

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3010, reload=True)