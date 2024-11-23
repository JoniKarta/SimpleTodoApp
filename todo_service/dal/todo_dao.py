from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuration.config import Config

config = Config()
engine = create_engine(url=config.DATABASE_URL)
session_local = sessionmaker(bind=engine, autoflush=False)


def get_todo_dao():
    session = session_local()
    try:
        yield session
        session.commit()
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.close()
