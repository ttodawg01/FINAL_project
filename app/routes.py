from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app import app
from app.forms import SignUpForm, LoginForm
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
        #check to see if user exists
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
        if check_user is not None:
            flash("User with username and/or email already exists", 'danger')
            return redirect(url_for('signup'))
        #add user to the database
        new_user = User(email=email, username=username, password=password)
        # flash a message
        flash(f"{new_user} has succesfully signed up!", 'success')

        #go back to the main page
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # get the form data
        username = form.username.data
        password = form.password.data
        #verify if their is a user with these credentials
        user = User.query.filter_by(username = username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user} is now logged in!", 'primary')
            return redirect(url_for('index'))
        else:
            flash('Incorrect Username/password. Please try again', 'danger')
            return redirect(url_for('login'))


    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))