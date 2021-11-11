from flask import Flask
from markupsafe import escape
from flask import render_template


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('materias-camara.html')#"<p><h1>Hello, World!</h1></p>"

@app.route('/')
def index():
    return 'Index Page'

@app.route("/<name>")
def hello(name):
    return f"<h2>Hello, {escape(name)}!</h2>"
