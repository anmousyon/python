'''controller class'''

import pprint
from database import Database
from reddit import Reddit
from cleaner import Cleaner


class Controller:
    '''controller for entire program'''
    def __init__(self):
        self.database = Database()

    def display_db(self):
        '''
        ***not meant to stay***
        display everything in database
        '''
        cleaner = Cleaner()
        for post in self.database.posts.find():
            loaded = cleaner.load(post)
            pprint.pprint(loaded.data)

        for comment in self.database.comments.find():
            loaded = cleaner.load(comment)
            pprint.pprint(loaded.data)

    def build(self):
        '''build the database'''
        reddit = Reddit()
        cleaner = Cleaner()
        for subreddit in reddit.get_subreddits():
            for post in reddit.get_posts(subreddit):
                self.database.insert(
                    cleaner.clean(post)
                )
                for comment in reddit.get_comments(post):
                    self.database.insert(
                        cleaner.clean(comment)
                    )
