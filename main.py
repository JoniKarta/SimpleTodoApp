import uvicorn
from fastapi import FastAPI

from common.database.base import Base
from common.database.repository import engine
from configuration.config import Config
from todo_service.controller import todo_controller
from user_service.controller import user_controller

app = FastAPI()

config = Config()

Base.metadata.create_all(bind=engine)

app.include_router(todo_controller.router, prefix=f'/api/{config.ROOT_PREFIX_VERSION}')
app.include_router(user_controller.router, prefix=f'/api/{config.ROOT_PREFIX_VERSION}')

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
