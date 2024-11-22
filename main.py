import uvicorn
from fastapi import FastAPI

from configuration.config import Config
from todo_service.controller import todo_controller

app = FastAPI()

config = Config()

app.include_router(todo_controller.router, prefix=f'/api/{config.ROOT_PREFIX_VERSION}')

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
