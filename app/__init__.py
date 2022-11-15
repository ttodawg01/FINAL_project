from flask import Flask


app = Flask(__name__)
#add a secret key to app config
app.config['SECRET_KEY'] = 'you-will-never-guess'


from . import routes