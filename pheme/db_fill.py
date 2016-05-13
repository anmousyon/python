import praw
from urllib.parse import urlparse
import re
import json
import requests
from .app import models
from textblob import TextBlob
from .app import views
import datetime

useless = ['and', 'the', 'a', 'i']

class sub():
	def __init__(self, sub_name):
		subscribers = 0
		name = sub_name

class site():
	def __init__(self):
		domain = ''
		url = ''

#read in keys from text file
def keys():
	key_list = []
	with open('keys.txt') as keys_file:
		key_list = keys_file.readlines()
	for key in key_list:
		key.strip()
	return key_list

#login to reddit using praw
def redditlogin(key_list):
	print(key_list)
	r = praw.Reddit('lily')
	r.login(key_list[0].strip(), key_list[1].strip(), disable_warning=True)
	return r

def getTime(time):
	return datetime.datetime.fromtimestamp(time)

def getComments(post):
	return praw.helpers.flatten_tree(post.comments)

def getSite(post):
	site_name = urlparse(post.url)[1]
	return 'http://' + site_name.strip()

def getSent(text):
	text = TextBlob(text)
	return text.sentiment.polarity

def getKeywords(text, useless):
	text = TextBlob(text)
	for word in text.words:
		for bad in useless:
			if word is bad:
				text.remove(word)
	return text


def fillPosts(sub_name, r):
	posts = r.get_subreddit(sub_name)
	for post in posts.get_hot(limit=5):
		site = getSite(post)
		comments = getComments(post)
		dt = getTime(post.created)
		subreddit = sub(sub_name)
		edited = getTime(post.edited)
		sentiment = fillComments(post, comments, r, site, subreddit, dt)
			
		to_add = app.models.Post(post.id, sentiment, comments, site, subreddit, post.author, dt, edited, post.score, post.gilded)
		#add to_add to db
		postsdb.session.add(to_add)
		

def fillComments(post, comments, r, site, subreddit, dt):
	sentiment_total = 0
	counter = 0
	for comment in comments:
		sentiment = getSent(comment.body)
		edited = getTime(comment.edited)		
		keywords = getKeywords(comment.body, useless)

		to_add = app.models.Comment(comment.body, sentiment, post.id, site, subreddit, comment.author, dt, edited, comment.score, comment.gilded, keywords)
		
		commentsdb.session.add(to_add)

		sentiment_total += sentiment
		counter += 1
	sentiment_total = sentiment_total / counter

def filldb(subs, r):
	for sub in subs:
		fillPosts(sub, r)

def main():
	subs = ['technology', 'news', 'worldnews', 'upliftingnews']
	postsdb.create_all()
	commentsdb.create_all()
	key = keys()
	r = redditlogin(key)
	filldb(subs, r)
	postsdb.commit()
	commentsdb.commit()

main()
