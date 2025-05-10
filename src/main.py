from flask import Flask

from src.blog_api.app import blog_api_bp
from src.weather_api.app import weather_api_bp
from src.chat_api.app import chat_api_pb
from src.db.base import create_database

app = Flask(__name__)


@app.after_request
def set_headers(response):
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5173"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["mode"] = "no-cors"


    return response


app.register_blueprint(blog_api_bp)
app.register_blueprint(weather_api_bp)
app.register_blueprint(chat_api_pb)

app.secret_key = "your_secret_key_here"

if __name__ == "__main__":
    with app.app_context():
        create_database()

    app.run(debug=True, port=5055)
