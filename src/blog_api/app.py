from flask import Blueprint, jsonify, Request, request

from src.util.database_helper import database_session
from src.db.models.blogs import BlogSchema
from src.db.services.blog import (
    add_blog,
    get_all_blog_data,
    delete_post_data,
    edit_post_data,
    get_post_data_by_id,
)


blog_api_bp = Blueprint("blog_api_bp", __name__, url_prefix="/api/blog")


@blog_api_bp.route("/post", methods=["GET"])
@database_session
def get_post(db_session) -> Request:

    id = request.args.get("id")
    post = get_post_data_by_id(db_session, id).to_dict()
    if post:
        res = jsonify(post)
        res.status_code = 200
    else:
        res = jsonify({"msg": "Post not found"})
        res.status_code = 404

    return res


@blog_api_bp.route("/posts", methods=["GET"])
@database_session
def get_all_post(db_session) -> Request:

    post = [post.to_dict() for post in get_all_blog_data(db_session)]
    if post:
        res = jsonify(post)
        res.status_code = 200
    else:
        res = jsonify({"msg": "Post not found"})
        res.status_code = 404

    return res


@blog_api_bp.route("/post", methods=["POST"])
@database_session
def add_post(db_session) -> Request:
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        res = jsonify({"msg": "Title and content are required"})
        res.status_code = 400
        return res

    blog = BlogSchema(
        title=title,
        content=content,
    )

    res = jsonify(add_blog(db_session, blog).to_dict())
    res.status_code = 201
    return res


@blog_api_bp.route("/post", methods=["PUT"])
@database_session
def edit_post(db_session) -> Request:
    data = request.get_json()

    id = data.get("id")
    title = data.get("title")
    content = data.get("content")

    blog = BlogSchema(
        title=title,
        content=content,
    )

    post_data = edit_post_data(db_session, id, blog)
    if post_data is None:
        res = jsonify({"msg": "Post not found"})
        res.status_code = 404
    else:
        res = jsonify(post_data.to_dict())
        res.status_code = 200

    return res


@blog_api_bp.route("/post", methods=["DELETE"])
@database_session
def delete_post(db_session) -> Request:
    id = request.args.get("id")

    try:
        delete_post_data(db_session, id)
        res = jsonify({"msg": "Post deleted successfully"})
        res.status_code = 200
    except Exception as e:
        res = jsonify({"msg": "Post not found"})
        res.status_code = 404
    return res


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(blog_api_bp)
    app.run(debug=True, port=5055)
