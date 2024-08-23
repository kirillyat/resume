from flask import Flask, render_template
import datetime

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template(
        "index.html", year=datetime.datetime.now().year, active_page="inde§x"
    )


@app.route("/contacts")
def contacts():
    return render_template(
        "contacts.html", year=datetime.datetime.now().year, active_page="contacts"
    )


@app.route("/about")
def about():
    return render_template(
        "about.html", year=datetime.datetime.now().year, active_page="about"
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", year=datetime.datetime.now().year), 404


if __name__ == "__main__":
    app.run()
