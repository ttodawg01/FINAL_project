from flask import Flask
#import sql achemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
#add a secret key to app config
app.config.from_object(Config)


# create db for database
db = SQLAlchemy(app)
# create migrate
migrate = Migrate(app, db)

from . import routes