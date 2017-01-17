import praw

#logon to praw

#check comment stream

class User:
    def __init__(user):
        username = user.username

class OP:
    def __init__(user):
        posts = user.posts
        comments = user.comments

class Requester:
    def __init__(user):
        posts = user.posts
        comments = user.comments
    
    def message():
        #message the requester

class Submission:
    def __init__(submission):
        request = submission.request
        user = submission.user
        link = submission.link
        created = submission.created
        score = submission.score
        gold = submission.gold
        edited = submission.edited

    def is_op(op):
        return op.username == submission.user.username

class Post:
    def __init__(post):
        subreddit = post.subreddit
        title = post.title
    

class Comment:
    def __init__(comment):
        body = comment.body


def checker(thread, requesters):
    #check a post or comment for an update

def check_for_edit(submission, requesters):
    if post.edited > request:
        return true

def check_for_comment(submission, requesters):
    for requester in requesters:
        if requester.comment.replied():
            return true

