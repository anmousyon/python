from app import postsdb, commentsdb
import praw
from db_fill import sub, site
import datetime

class Comment(commentsdb.Model):
	id = commentsdb.Column(db.Integer, primary_key=True)
	comment = commentsdb.Column(db.String(400))
	sentiment = commentsdb.Column(db.Float)
	post = commentsdb.relationship('Post', backref='author', lazy='dynamic')
	site = commentsdb.Column(db.String(200))
	sub = commentsdb.Column(db.String(50))
	user = commentsdb.Column(db.String(100))
	dt = commentsdb.Column(db.DateTime)
	edit = commentsdb.Column(db.DateTime)
	karma = commentsdb.Column(db.Integer)
	gold = commentsdb.Column(db.Integer)
	keywords = commentsdb.Column(db.Array)
	
def __repr__(self):
		return '<User %r>' % (self.sentiment)

class Post(postsdb.Model):
	id = postsdb.Column(db.Integer, primary_key=True)	
	postid = postsdb.Column(db.Integer)
	sentiment = postsdb.Column(db.Integer)
	comments = postsdb.Column(db.Array)
	site = postsdb.Column(db.String(200))
	sub = postsdb.Column(db.String(50))
	user = postsdb.Column(db.String(100))
	dt = postsdb.Column(db.datetime)
	edited = postsdb.Column(db.datetime)
	karma = postsdb.Column(db.Integer())
	gold = postsdb.Column(db.Integer())

	def __repr__(self):
		return '<Post %r>' % (self.sentiment)
