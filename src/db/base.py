from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

uri = "sqlite:///memory.db"
Engine = create_engine(uri)
localsession = sessionmaker(bind=Engine, autoflush=True)

class Base(DeclarativeBase):
    pass

def create_database():
    Base.metadata.create_all(Engine)