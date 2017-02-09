'''cleaner class'''

from models import Post, Comment, PostSchema, CommentSchema
import praw
from analyzer import Analyzer


class Cleaner:
    '''cleans items and dumps/loads them with marshmallow'''
    def __init__(self):
        self.post_schema = PostSchema()
        self.comment_schema = CommentSchema()
        self.analyzer = Analyzer()

    def clean(self, item):
        '''clean a dirty object then dump it'''
        if isinstance(item, praw.models.Submission):
            dirty = Post(item)
            dirty.title_sentiment = self.analyzer.sentiment(item.title)
        elif isinstance(item, praw.models.Comment):
            dirty = Comment(item)
            dirty.body_sentiment = self.analyzer.sentiment(item.body)
        else:
            raise TypeError(
                "clean only takes praw.models.Submission \
                and praw.models.Comment objects"
            )
        cleaned = self.dump(dirty)
        return cleaned

    def dump(self, item):
        '''dump a clean object into dict'''
        if isinstance(item, Post):
            dumped = self.post_schema.dump(item)
        elif isinstance(item, Comment):
            dumped = self.comment_schema.dump(item)
        else:
            raise TypeError("dump only takes Comment and Post objects")
        return dumped

    def load(self, item):
        '''load clean object from dict'''
        if isinstance(item, dict):
            if 'title_sentiment' in item:
                loaded = self.post_schema.load(item)
            elif 'body_sentiment' in item:
                loaded = self.comment_schema.load(item)
        else:
            raise TypeError(
                "load only takes dict objects"
            )
        return loaded
