import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import declarative_base

from configuration.config import Config
from todo_service.controller import todo_controller
from todo_service.dal.todo_dao import engine

app = FastAPI()

config = Config()

declarative_base().metadata.create_all(bind=engine)

app.include_router(todo_controller.router, prefix=f'/api/{config.ROOT_PREFIX_VERSION}')

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
