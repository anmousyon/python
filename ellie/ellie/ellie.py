import collections


class Reddit:
    def __init__():
        client = praw.Reddit('lily')

    def load_credentials():
        with open('ellie/info/keys.txt') as keys_file:
            keys = file.readlines()
        credentials = collections.namedtuple(
            username=keys[0].strip(),
            password=keys[1].strip()
        )
        return credentials

    def login():
        credentials = load_credentials()
        client.login(
            credentials.username,
            credentials.password,
            disable_warnings=True
        )

class Subreddit(Reddit):
    def __init__(name):
        name = name

    def get_posts():
        submissions = [post for post in reddit.get_subreddit(name).get_hot(limit=20)]

    def add_to_db():
        for submission in submissions:
            post = Submission(submission)
            post.add_to_db


class Submission:

    def __init__(submission):
        post_id = submission.id

    def get_image()

