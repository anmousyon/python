'''models for builder'''

from marshmallow import Schema, fields


class Submission:
    '''parent class for all submissions'''
    def __init__(self, item):
        self.label = str(item.id)
        self.subreddit = str(item.subreddit)
        self.username = str(item.author)
        self.score = str(item.score)


class PostSchema(Schema):
    '''marshmallow schema for posts'''
    label = fields.Str()
    subreddit = fields.Str()
    username = fields.Str()
    score = fields.Str()
    title_sentiment = fields.Str()


class Post(Submission):
    '''hold specific post info'''
    def __init__(self, post):
        super().__init__(post)
        self.title_sentiment = None


class CommentSchema(Schema):
    '''marshmallow schema for comments'''
    label = fields.Str()
    subreddit = fields.Str()
    username = fields.Str()
    score = fields.Str()
    body_sentiment = fields.Str()


class Comment(Submission):
    '''hold specific comment info'''
    def __init__(self, comment):
        super().__init__(comment)
        self.body_sentiment = None
