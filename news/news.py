import newspaper
from newspaper import Article
from newspaper import fulltext
import praw
from urllib.parse import urlparse
import re
import json
import requests

def keys():
    key = []
    with open('keys.txt') as keys_file:
        key = keys_file.readlines()
    return key

def redditlogin(key):
    r = praw.Reddit('news checker')
    r.login(key[1], key[2])
    return r

def readSites():
    with open('sites.txt') as sites_file:
        sites = [word.strip() for word in sites_file]
    return sites

def makeSiteDict(sites):
    site_dict = {}
    for site in sites:
        site_dict.update({site:None})
    return site_dict

def makePostDict(posts):
    post_dict = {}
    for post in posts.get_hot(limit=5):
        post_dict.update({post.title:post})
    return post_dict

def makeSentimentDict(posts):
    sentiment_dict = {}
    for post in posts:
        sentiment_dict.update({post:None})
    return sentiment_dict

def check_and_add_http(url):
    # checks if 'http://' is present at the start of the URL and adds it if not.
    http_regex = re.compile(r'^http[s]?://')
    if http_regex.match(url):
        # 'http://' or 'https://' is present
        return url
    else:
        # add 'http://' for urlparse to work.
        return 'http://' + url

def from_important(site, sites):
    #print(sites)
    if site in sites:
        return True

def getPostContent(sub_name, reddit, list_of_sites, site_dict):
    posts = reddit.get_subreddit(sub_name)
    for post in posts.get_hot(limit=5):
        site_name = post.url
        site_name = urlparse(site_name)[1]
        #check_and_add_http(site_name)
        site_name = 'http://' + site_name.strip()
        #print(site_name)
        if not site_name in site_dict:
            site_dict.update({site_name:None})
        if not site_dict[site_name]:
            site_dict[site_name] = post.title
    return site_dict

def crosscheck(sentiment_dict):
    site_sentiment_dict = {}
    for post in sentiment_dict:
        site_sentiment_dict.update({sentiment_dict[post][0]:sentiment_dict[post][1]})
    return site_sentiment_dict

def checkSentiment(posts, site_dict, sentiment_dict):
    for post in posts:
        post_id = posts[post]
        pos = 0
        neg = 0
        neut = 0
        top = ''
        flat_comments = praw.helpers.flatten_tree(post_id.comments)
        flat_comments[:1]
        comments_dict.update({post:None})
        for comment in flat_comments:
            if not isinstance(comment, praw.objects.MoreComments):
                commenttext = ("text=" + (comment.body).strip()).encode("utf-8")
                #print(commenttext)
                #url = "http://text-processing.com/api/sentiment/"
                #json_result = requests.post(url, data=commenttext)
                #parsed_json = json_result.json()
                #rating = parsed_json['label']
                rating = 'pos'
                rating = rating.strip()
                #print(parsed_json['label'])
                if(rating == 'pos'):
                    pos += 1
                elif(rating == 'neg'):
                    neg += 1
                elif(rating == 'neutral'):
                    neut += 1
                top = max(pos, neg, neut)
                comments_dict[post] = list()
                comments_dict[post].append((comment.body.strip()).encode("utf-8"))
        if(top == pos):
            top = 'pos'
        elif(top == neg):
            top ='neg'
        elif(top == neut):
            top = 'neutral'
        site_name = 'http://' + urlparse(posts[post].url)[1].strip()
        sentiment_dict[post] = [site_name, top]
    return sentiment_dict

def print_sentiment_dict(sd):
    for x in sd:
        print(x[:50] + "...")
        print(sd[x][1])
        print()

def print_site_sentiment_dict(ssd):
    for x in ssd:
        print(x[:50] + "...")
        print(ssd[x])
        print()

def print_pos_comment_dict(cd, sentiment_dict):
    for post in sentiment_dict:
        if(sentiment_dict[post][1][:50] == 'pos'):
            for x in cd[post]:
                print(x)
            return;

key = []
site_list = []
site_dict = {}
posts_list = []
sentiment_dict = {}
comments_dict = {}

def feeling(sub_name):
    key = keys()
    r = redditlogin(key)
    site_list = readSites()
    site_dict = makeSiteDict(site_list)
    #print(site_dict)
    posts_list = r.get_subreddit(sub_name)
    post_dict = makePostDict(posts_list)
    site_dict = getPostContent(sub_name, r, site_list, site_dict)
    sentiment_dict = makeSentimentDict(post_dict)
    sentiment_dict = checkSentiment(post_dict, site_dict, sentiment_dict)
    print_sentiment_dict(sentiment_dict)
    #newspaper = getNewspaperContent()
    site_sentiment_dict = crosscheck(sentiment_dict)
    print_site_sentiment_dict(site_sentiment_dict)
    print_pos_comment_dict(comments_dict, sentiment_dict)
    return 'done'

sub = input('Which subreddit do you want to analyse? ')
print('Alright, hold on a bit.')
tasks = [feeling]
data = str(sub.strip())
print(data)
feeling(data)