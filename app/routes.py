from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def post():
    return render_template("posts.html")