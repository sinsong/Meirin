from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from meirin.server.config import settings

# echo=True
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# https://docs.sqlalchemy.org/en/14/tutorial/engine.html
Session = sessionmaker(bind=engine)
