import datetime
import os

import markdown
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


admin = Admin(app, name="My Admin", template_mode="bootstrap4", endpoint="/admin")
admin.add_view(ModelView(Post, db.session))

with app.app_context():
    db.create_all()


@app.route("/post/<int:id>")
def post(id):
    post = Post.query.get(id)
    post.text = markdown.markdown(post.text)
    return render_template("post.html", year=datetime.datetime.now().year, post=post)


@app.route("/")
@app.route("/index")
def index():
    return render_template(
        "blog.html",
        year=datetime.datetime.now().year,
        active_page="index",
        posts=Post.query.all(),
    )


@app.route("/contacts")
def contacts():
    return render_template(
        "contacts.html", year=datetime.datetime.now().year, active_page="contacts"
    )


@app.route("/about")
def about():
    experience = [
        {
            "company": "Avito Tech",
            "start_date": "Oct 2023",
            "end_date": "Today",
            "description": "Software engineer",
        },
        {
            "company": "Yandex Taxi",
            "start_date": "Aug 2021",
            "end_date": "Sep 2023",
            "description": "Software engineer",
        },
        {
            "company": "Sber Tech",
            "start_date": "Nov 2020",
            "end_date": "May 2021",
            "description": "Data-engineer",
        },
    ]

    education = [
        {
            "institution": "ITMO University",
            "start_date": "2023",
            "end_date": "2025",
            "degree": "Master’s Degree in Computer Science",
        },
        {
            "institution": "Lomonosov Moscow State University (MSU)",
            "start_date": "2018",
            "end_date": "2022",
            "degree": "Bachelor's Degree in Computer Science",
        },
    ]

    skills = [
        "Golang",
        "PHP",
        "ClickHouse",
        "Python",
        "C++",
        "PostgreSQL",
    ]

    return render_template(
        "about.html",
        year=datetime.datetime.now().year,
        active_page="about",
        experience=experience,
        education=education,
        skills=skills,
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", year=datetime.datetime.now().year), 404


if __name__ == "__main__":
    app.run()
