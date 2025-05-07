from flask import Flask, jsonify, Request, request, render_template, url_for, redirect
from datetime import datetime

from src.blog_api.db.service import (
    add_blog,
    get_all_blog_data,
    delete_post_data,
    edit_post_data,
    get_post_data_by_id,
)
from src.blog_api.db.models.blogs import BlogSchema
from src.blog_api.db.base import Base, Engine, localsession

Base.metadata.create_all(Engine)
session = localsession()

app = Flask(__name__)


@app.get("/post")
def get_post() -> Request:
    id = request.args.get("id")
    post = get_post_data_by_id(session, id).to_dict()
    if post:
        res = jsonify(post)
        res.status_code = 200
    else:
        res = jsonify({"message": "Post not found"})
        res.status_code = 404
    res.headers["Content-Type"] = "application/json"

    return res


@app.get("/post/getall")
def get_all_post() -> Request:

    post = [post.to_dict() for post in get_all_blog_data(session)]
    if post:
        res = jsonify(post)
        res.status_code = 200
    else:
        res = jsonify({"message": "Post not found"})
        res.status_code = 404
    res.headers["Content-Type"] = "application/json"

    return res


@app.post("/post")
def add_post() -> Request:

    title = request.form.get("title")
    content = request.form.get("content")

    if title and content:
        blog = BlogSchema(
            title=title,
            content=content,
        )

        jsonify(add_blog(session, blog).to_dict())

    return redirect(url_for("home"), 301)


@app.put("/post")
def edit_post() -> Request:
    data = request.get_json()

    id = data.get("id")
    title = data.get("title")
    content = data.get("content")

    blog = BlogSchema(
        title=title,
        content=content,
    )

    post_data = edit_post_data(session, id, blog)
    if post_data is None:
        res = jsonify({"message": "Post not found"})
        res.status_code = 404
    else:
        res = jsonify(post_data.to_dict())
        res.status_code = 200

    res.headers["Content-Type"] = "application/json"
    return res


@app.route("/post", methods=["DELETE", "GET"])
def delete_post() -> Request:
    id = request.args.get("id")
    delete_post_data(session, id)
    return jsonify({"message": "Post deleted successfully"})


def time_format(post_data: dict[str, any]) -> str:
    last_modified_dt_str = post_data["last_modified"]
    created_at_dt_str = post_data["created_at"]

    post_data["last_modified"] = last_modified_dt_str.strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    post_data["created_at"] = created_at_dt_str.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return post_data


@app.route("/", methods=["GET"])
def home():

    posts = [time_format(post.to_dict()) for post in get_all_blog_data(session)]

    return render_template("index.html", posts=posts)


if __name__ == "__main__":
    from src.blog_api.db.base import create_engine, sessionmaker

    Engine = create_engine("sqlite:///demo.db")
    Base.metadata.create_all(Engine)
    localsession = sessionmaker(bind=Engine, autoflush=True)
    session = localsession()
    app.run(debug=True)
    url_for("home", _method="GET")
