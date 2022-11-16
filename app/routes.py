from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import SignUpForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def post():
    return render_template("posts.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('success')
        #data from the form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        #add user to the database
        new_user = User(email=email, username=username, password=password)
        # flash a message
        flash(f"{new_user} has succesfully signed up!", 'success')

        #go back to the main page
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)