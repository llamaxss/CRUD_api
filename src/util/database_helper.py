from functools import wraps

from src.db.base import localsession


def database_session(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        with localsession() as db_session:
            try:
                result = func(db_session=db_session, *args, **kwargs)
                return result
            except Exception as e:
                db_session.rollback()
                raise e

    return wrapper
