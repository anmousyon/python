import praw
from urllib.parse import urlparse
import re
import json
import requests
from models import Comment, Post
from textblob import TextBlob

class sub():
	def __init__(self, sub_name):
		subscribers = 0
		name = sube_name

class sentiment():
	def __init__(self):
		pos = 0
		neg = 0
		neut = 0
		sent = 0

class edited():
	def __init__(self):
		edited = false
		lastEdited = ''

class site():
	def __init__(self):
		domain = ''
		url = ''

subs = []
articles = []
users = []
sites = []

#read in keys from text file
def keys():
	key = []
	with open('keys.txt') as keys_file:
		key = keys_file.readlines()
	return key

#login to reddit using praw
def redditlogin(key):
	r = praw.Reddit('lily')
	r.login(key[1], key[2], disable_warning=True)
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
	return text.sentiment


def fillPosts(sub_name, r):
	posts = reddit.get_subreddit(sub_name)
	for post in posts:
		site = getSite(post)
		sentiment = getSent(
		comments = getComments(post)
		dt = getTime(post.created)
		subreddit = sub(sub_name)
		edited = getTime(post.edited)
		sentiment = fillComments(post, comments, r, site, subreddit, dt)
			
		to_add = Post(post, sentiment, comments, site, subreddit, post.author, dt, edited, post.score, post.gilded)
		#add to_add to db
		

def fillComments(post, comments, r, site, subreddit, dt):
	sentiment_total = 0
	counter = 0
	for comment in comments:
		sentiment = getSent(comment.body)
		edited = getTime(comment.edited)		
		aillComments(post, comments, r, site, subreddit, dt)

		to_add = Comment(comment, sentiment, post, site, subreddit, comment.author, dt, edited, comment.score, comment.gilded)
		
		sentiment_total += sentiment.polarity
		counter += 1
	sentiment_total = sentiment_total / counter

def filldb(subs, r):
	for sub in subs:
		fillPosts(sub, r)
