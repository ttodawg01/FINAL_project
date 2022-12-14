from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import SignUpForm, LoginForm, PostForm
from app.models import User, Post
import requests
from requests import Session
import json
import API.api as secrets
from newsapi import NewsApiClient
# from secrets2 import API_KEY2
from flask_mail import Mail, Message


class Crypto:
    def get_top_5(self): #method for the top 5

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

    def get_top_15(self): #method to get the top 10 cyrptocurrencies

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
          'start':'1',
          'limit':'15',  #top 15 cryptocurrencies
          'convert':'USD'  #translated to be read in us sollar currency
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': secrets.API_KEY,  #hide my api key
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data']
#im returning the data right here so i have access to the other important details associated with the crypto coin
#returns an array


@app.route('/')
def index():
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
    # msg = Message('Confirm email', sender='ttodawg@outlook.com', recipients=[email])

    # link = url_for('confirm_email', _external=True)

    # msg.body = 'your link is {}'.format(link)

    # mail.send(msg)

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



@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    if post.author != current_user:  #you cannot edit a post if you did not make the post
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        # Get form data
        new_title = form.title.data
        new_body = form.body.data
        # update the post
        post.update(title=new_title, body=new_body)  
        flash(f"{post.title} has been updated", "success")
        return redirect(url_for('get_post', post_id=post.id))
    return render_template('edit_post.html', post=post, form=form)



@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('index'))
    post.delete()
    flash(f"{post.title} has been deleted", 'info')
    return redirect(url_for('index'))

@app.route('/crypto')
@login_required
def crypto():
    crypto = Crypto()  #calling the class 

    results = crypto.get_top_15() #calling the method to get the top 15 crypto in the market

    for result in results:
        result['quote']['USD']['price'] = '$ ' + "{:.2f}".format(result['quote']['USD']['price']) 
        #as i loop through my results it will return the coin individually and format to 2 decimal places

    return render_template('crypto.html', **locals())
    #export on the locals** without this my data does now show up


@app.route('/news')
@login_required
def news():
    newsapi = NewsApiClient(api_key='27d11cfca0cc47ceb72d57376f89f5aa')
    topheadlines = newsapi.get_top_headlines()
 
    articles = topheadlines['articles']
 
    desc = []
    news = []
    img = []
 
    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
 
    mylist = zip(news, desc, img)
    return render_template('news.html', context = mylist)