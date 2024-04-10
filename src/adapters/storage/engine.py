from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session_factory(uri):
    engine = create_engine(uri, pool_size=20, max_overflow=0, pool_pre_ping=False)
    return sessionmaker(bind=engine)
