from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from . import *

app = Flask(__name__)
app.config.from_object('config')
postsdb = SQLAlchemy(app)
commentsdb = SQLAlchemy(app)

from app import views, models

