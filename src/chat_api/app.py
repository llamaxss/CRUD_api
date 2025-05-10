from flask import request, jsonify, session, Blueprint

from src.util.database_helper import database_session
from src.db.services.chat import login_user, is_duplicate_user, create_user

chat_api_pb = Blueprint("chat_api_pb", __name__, url_prefix="/api/chat")


@chat_api_pb.route("/auth", methods=["POST"])
@database_session
def login(db_session):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = login_user(session=db_session, username=username, password=password)
    if user:
        session["username"] = username
        res = jsonify(username=username)
        res.status_code = 200
    else:
        res = jsonify(error="Invalid credentials")
        res.status_code = 401

    return res


@chat_api_pb.route("/logout", methods=["POST"])
def logout():
    session.clear()
    res = jsonify(message="Logged out successfully")
    res.status_code = 200
    return res


@chat_api_pb.route("/register", methods=["POST"])
@database_session
def register(db_session):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        res = jsonify(error="Username and password are required")
        res.status_code = 400
        return res

    user = is_duplicate_user(session=db_session, username=username)
    if user:
        res = jsonify(error="Username already exists")
        res.status_code = 409
        return res
    else:
        try:
            _ = create_user(session=db_session, username=username, password=password)
            session["username"] = username
            res = jsonify(username=username)
            res.status_code = 201
        except Exception as e:
            res = jsonify(error="Error creating user")
            res.status_code = 500
        return res
