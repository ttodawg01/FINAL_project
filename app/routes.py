from flask import render_template
from app import app
from app.forms import SignUpForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def post():
    return render_template("posts.html")

@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)