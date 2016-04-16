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
'''
def getNewspaperContent():
    bn = newspaper.build('http://breakingnews.com') 
    for article in bn.articles:
        print(article.url)
    for category in bn.category_urls():
        print(category)
    return bn
'''
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
    for post in posts.get_hot(limit=15):
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
    else:
        print('not in list')

def getPostContent(reddit, list_of_sites, site_dict):
    posts = reddit.get_subreddit('worldnews')
    for post in posts.get_hot(limit=15):
        site_name = post.url
        site_name = urlparse(site_name)[1]
        #check_and_add_http(site_name)
        site_name = 'http://' + site_name.strip()
        print(site_name)
        if from_important(site_name, list_of_sites):
            print('added')
            if not site_dict[site_name]:
                site_dict[site_name] = list()
                site_dict[site_name].append(post.title)
            else:
                site_dict[site_name].append(post.title)
    return site_dict

def crosscheck(sites, site_dict):
    for site in sites:
        if site in site_dict.keys():
            print(site)
            print(site_dict[site])

def checkSentiment(posts, sentiment_dict):
    for post in posts:
        post_id = posts[post]
        pos = 0
        neg = 0
        neut = 0
        top = ''
        flat_comments = praw.helpers.flatten_tree(post_id.comments)
        for comment in flat_comments:
            if not isinstance(comment, praw.objects.MoreComments):
                commenttext = ("text=" + (comment.body).strip()).encode("utf-8")
                url = "http://text-processing.com/api/sentiment/"
                json_result = requests.post(url, data=commenttext)
                parsed_json = json_result.json()
                rating = parsed_json['label']
                rating = rating.strip()
                print(parsed_json['label'])
                if(rating == 'pos'):
                    pos += 1
                elif(rating == 'neg'):
                    neg += 1
                elif(rating == 'neutral'):
                    neut += 1
                print('pos = {}'.format(pos))
                print('neg = {}'.format(neg))
                print('neutral = {}'.format(neut))
                top = max(pos, neg, neut)
        if(top == pos):
            top = 'pos'
        elif(top == neg):
            top ='neg'
        elif(top == neut):
            top = 'neutral'
        sentiment_dict[post] = top
    return sentiment_dict

def main():
    key = keys()
    r = redditlogin(key)
    site_list = readSites()
    site_dict = makeSiteDict(site_list)
    print(site_dict)
    posts_list = r.get_subreddit('worldnews')
    post_dict = makePostDict(posts_list)
    sentiment_dict = makeSentimentDict(post_dict)
    sentiment_dict = checkSentiment(post_dict, sentiment_dict)
    print(sentiment_dict)
    #newspaper = getNewspaperContent()
    site_dict = getPostContent(r, site_list, site_dict)
    crosscheck(site_list, site_dict)

    print('done')

main()