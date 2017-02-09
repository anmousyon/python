'''database class'''

from pymongo import MongoClient
from marshmallow import MarshalResult


class Database:
    '''manages the database'''
    def __init__(self):
        self.client = MongoClient()
        self.posts, self.comments = self.load()

        # emptying database before each run for now
        self.clear()

    def clear(self):
        '''clear database tables'''
        self.posts.delete_many({})
        self.comments.delete_many({})

    def load(self):
        '''load tables from database'''
        database = self.client.database
        return database.posts, database.comments

    def insert(self, item):
        '''insert item into database'''
        if isinstance(item, MarshalResult):
            if 'title_sentiment' in item.data:
                self.posts.insert_one(item.data)
            elif 'body_sentiment' in item.data:
                self.comments.insert_one(item.data)
        else:
            print(item.data)
            raise TypeError(
                "insert only takes MarshalResult objects"
            )
