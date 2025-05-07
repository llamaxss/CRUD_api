from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

uri = ":memory:"
Engine = create_engine(f"sqlite:///{uri}")
localsession = sessionmaker(bind=Engine, autoflush=True)

class Base(DeclarativeBase):
    pass