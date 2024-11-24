from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuration.config import Config

config = Config()
engine = create_engine(url=config.DATABASE_URL, echo=True)
session_local = sessionmaker(bind=engine, autoflush=False)
