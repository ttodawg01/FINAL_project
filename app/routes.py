from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import SignUpForm, LoginForm, PostForm
from app.models import User, Post
import requests
from requests import Session
import json
import API.api as secrets


class Crypto:

    def get_top_5(self):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
          'start':'1',
          'limit':'5',
          'convert':'USD'
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': secrets.API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data']

    def get_top_10(self):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
          'start':'1',
          'limit':'10',
          'convert':'USD'
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': secrets.API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data']



@app.route('/')
def index():
    crypto = Crypto()

    results = crypto.get_top_10()

    # for result in results:
    #     result['quote']['USD']['price'] = '$ ' + "{:.2f}".format(result['quote']['USD']['price'])

    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)

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


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        # Get the data from the form
        title = form.title.data
        body = form.body.data
        new_post = Post(title=title, body=body, user_id=current_user.id)
        # flash a message 
        flash(f"{current_user} just posted!", "success")
        # Redirect back to the home page
        return redirect(url_for('index'))

    return render_template('create.html', form=form)

@app.route('/posts/<post_id>') #lets us be able to see a specefic post
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    return render_template('post.html', post=post)