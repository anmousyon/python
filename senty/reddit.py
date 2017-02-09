'''reddit class'''

import praw


class Reddit:
    '''client for reddit api'''
    def __init__(self):
        self.client = self.login()

    def login(self):
        '''login to reddit client'''
        with open('keys.txt') as file:
            keys = file.readlines()
        return praw.Reddit(
            client_id=keys[0].strip(),
            client_secret=keys[1].strip(),
            user_agent=keys[2].strip()
        )

    def get_subreddits(self):
        '''create list of subreddit objects from file of subreddits'''
        with open('subreddits.txt') as file:
            subreddits = file.readlines()
        subreddits = [
            self.client.subreddit(subreddit.strip()) for subreddit in subreddits
        ]
        return subreddits[:5]

    def get_posts(self, subreddit):
        '''get all posts from subreddit object'''
        return [post for post in subreddit.hot(limit=5)]

    def get_comments(self, post):
        '''get all comments of post in list'''
        post.comments.replace_more(limit=1, threshold=10)
        return post.comments.list()
