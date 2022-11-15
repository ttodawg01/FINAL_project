from flask import Flask


app = Flask(__name__)
#add a secret key to app config
app.config['SECRET_KEY'] = 'Never-guess'


from . import routes