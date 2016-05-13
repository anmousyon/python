from app import db

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	comment = db.Column()#comment struct
	sentiment = db.Column()#sentiment struct
	post = db.relationship('Post', backref='author', lazy='dynamic')
	site = db.Column()#site struct
	sub = db.Column()#sub struct
	user = db.Column(db.String(100))
	dt = db.Column()#date and time struct
	edit = db.Column()#edited struct
	karma = db.Column(db.Integer)
	gold = db.Column(db.Integer)
	keywords = db.Column()#array of string
	
def __repr__(self):
		return '<User %r>' % (self.sentiment)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	post = db.Column()#post struct
	sentiment = db.Column()#sentiment struct
	comments = db.Column()#comment struct
	site = db.Column(_#site struct
	sub = db.Column()#sub struct
	user = db.Column(db.String(100))
	dt = db.Column(db.datetime)
	edited = db.Column()#edited struct
	karma = db.Column(db.Integer())
	gold = dbColumn(db.Integer())

	def __repr__(self):
		return '<Post %r>' % (self.sentiment)
