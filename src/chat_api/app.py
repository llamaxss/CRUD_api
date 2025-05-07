from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    session,
    Response,
)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "your_secret_key_here"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatdb.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


@app.route("/", methods=["GET"])
def home():
    if session.get("username"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session["username"] = username
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("home"))


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return redirect(url_for("home"))

    user = User.query.filter_by(username=username).first()
    if user:
        return redirect(url_for("home"))
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = username
        return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if username := session.get("username"):
        return render_template("dashboard.html", username=username)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
