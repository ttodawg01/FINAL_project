from flask import Flask
#import sql achemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
#add a secret key to app config
app.config.from_object(Config)


# create db for database
db = SQLAlchemy(app)
# create migrate
migrate = Migrate(app, db)
#let our app allow login capability
login = LoginManager(app)

from . import routes, models