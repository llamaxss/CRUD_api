from sqlalchemy.orm import Session
from datetime import datetime
from random import random

from ..models.chat_api import User


def login_user(session: Session, username: str, password: str) -> bool:
    user = session.query(User).filter_by(username=username, password=password).first()
    return user is not None


def is_duplicate_user(session: Session, username: str) -> bool:
    user = session.query(User).filter_by(username=username).first()
    return user is not None


def create_user(session: Session, username: str, password: str) -> User:

    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
