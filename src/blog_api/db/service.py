from sqlalchemy.orm import Session
from datetime import datetime
from random import random

from .models.blogs import BlogDb, BlogSchema


def add_blog(session: Session, blog: BlogSchema) -> BlogDb:
    blog_post = BlogDb(
        id= random(),
        title=blog.title,
        content=blog.content,
        last_modified=blog.last_modified,
        created_at=blog.last_modified,
    )
    session.add(blog_post)
    session.commit()
    session.refresh(blog_post)

    return blog_post


def edit_post_data(session: Session, id: str, blog: BlogSchema) -> BlogDb | None:
    post_data = get_post_data_by_id(session, id)
    if post_data is None:
        return None
    else:
        post_data.title = blog.title if blog.title is not None else post_data.title 
        post_data.content = blog.content if blog.content is not None else post_data.content
        post_data.last_modified = datetime.now()
        session.commit()
        session.refresh(post_data)

        return post_data


def get_post_data_by_id(session: Session, id: str) -> BlogDb | None:

    post_data = session.query(BlogDb).filter(BlogDb.id == id).first()
    if post_data is None:
        return None
    return post_data


def delete_post_data(session: Session, id: str) -> list[BlogDb]:
    post_data = get_post_data_by_id(session, id)
    if post_data is None:
        return None
    else:
        session.delete(post_data)
        session.commit()

        return post_data


def get_all_blog_data(session: Session) -> list[BlogDb]:
    return session.query(BlogDb).all()

def delete_all_blog_data(session: Session) -> None:
    try:
        session.query(BlogDb).delete()
        session.commit()
    except Exception as e:
        session.rollback()
