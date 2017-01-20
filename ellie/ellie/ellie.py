'''build databsase of comments and posts from reddit'''

import collections
import praw
from marshmallow import Schema, fields
from pymongo import MongoClient



class Database:
    def __init__(self):
        self.client = MongoClient()
        self.selfposts = None
        self.linkposts = None
        self.comments = None
        self.load()
    
    def load(self):
        self.db = self.client.db
        self.selfposts = self.db.selfposts
        self.linkposts = self.db.linkposts
        self.comments = self.db.comments


class LinkPostSchema(Schema):
    label = fields.Str()
    subreddit = fields.Str()
    username = fields.Str()
    score = fields.Int()
    link = fields.Str()
    title_sentiment = fields.Str()

class SelfPostSchema(Schema):
    label = fields.Str()
    subreddit = fields.Str()
    username = fields.Str()
    score = fields.Int()
    link = fields.Str()
    title_sentiment = fields.Str()
    selftext_sentiment = fields.Str()

class CommentSchema(Schema):
    label = fields.Str()
    subreddit = fields.Str()
    username = fields.Str()
    score = fields.Int()
    link = fields.Str()
    body_sentiment = fields.Str()


class Submission:
    '''superclass for all submission objects'''
    def __init__(self, submission):
        self.label = submission.id
        self.subreddit = submission.subreddit
        self.user = submission.author
        self.score = submission.score


class Post(Submission):
    '''superclass for all post objects'''
    def __init__(self, post):
        Submission.__init__(self, post)
        self.link = post.permalink
        self.post = post
        self.title_sentiment = None
        self.comments = None

    def add_to_db(self):
        '''add the post to the database'''
        self.get_comments()
        for comment in self.comments:
            to_add = Comment(comment)
            to_add.add_to_db()

    def get_comments(self):
        '''make a list from post's comment tree'''
        self.post.comments.replace_more(limit=1, threshold=10)
        self.comments = self.post.comments.list()


class SelfPost(Post):
    '''selfpost objects'''
    def __init__(self, post):
        Post.__init__(self, post)
        self.is_self = True
        self.selftext_sentiment = None

    def add_to_db(self):
        '''add selfpost to db'''
        Post.add_to_db(self)
        schema = SelfPostSchema()
        result = schema.dump(self)


class LinkPost(Post):
    '''linkpost objects'''
    def __init__(self, post):
        Post.__init__(self, post)
        self.is_self = False

    def add_to_db(self):
        '''add linkpost to db'''
        Post.add_to_db(self)


class Comment(Submission):
    '''comment objects'''
    def __init__(self, comment):
        Submission.__init__(self, comment)
        self.body_sentiment = None

    def add_to_db(self):
        '''add comment to db'''
        print(self.label)
        # figure out databse system to use


class Reddit:
    '''reddit object'''
    def __init__(self):
        self.client = None
        self.credentials = None
        self.subreddits = []

    def load_credentials(self):
        '''read and store reddit credentials'''
        keys = []
        with open('keys.txt') as keys_file:
            keys = keys_file.readlines()
            credentials = collections.namedtuple(
                'credentials',
                ['id', 'secret', 'user_agent']
            )
        self.credentials = credentials(
            id=keys[0].strip(),
            secret=keys[1].strip(),
            user_agent=keys[2].strip()
        )

    def login(self):
        '''load credentials and authorize reddit client'''
        self.load_credentials()
        self.client = praw.Reddit(
            client_id=self.credentials.id,
            client_secret=self.credentials.secret,
            user_agent=self.credentials.user_agent
        )

    def load_subreddits(self):
        '''read and store subreddits to query'''
        subs = []
        with open('subreddits.txt') as subs_file:
            subs = subs_file.readlines()
        self.subreddits = [
            subreddit.strip() for subreddit in subs
        ]

    def build(self):
        '''build database'''
        self.load_subreddits()
        for name in self.subreddits:
            subreddit = Subreddit(name, self)
            subreddit.get_posts()
            subreddit.add_to_db()


class Subreddit(Reddit):
    '''subreddit objects'''
    def __init__(self, name, reddit):
        super().__init__()
        self.name = name
        self.reddit = reddit
        self.posts = None

    def get_posts(self):
        '''retrieve posts from subreddit'''
        self.posts = [
            post for post in self.reddit.client.subreddit(self.name).hot(limit=20)
        ]

    def add_to_db(self):
        '''add post and comments to database'''
        for post in self.posts:
            if post.is_self:
                to_add = SelfPost(post)
            else:
                to_add = LinkPost(post)
            to_add.add_to_db()


def build():
    '''build comment and post databases'''
    reddit = Reddit()
    reddit.login()
    reddit.build()

build()
