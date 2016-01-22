#! python

import time
import re
import pickle
import praw
import tweepy
from pyshorteners import Shortener

postedTweets = []

redditObj = praw.Reddit('score poster')
redditObj.login('anmousyony', 'buffalo12')

keys = []

with open('keys.txt') as keys_file:
        keys = keys_file.readlines()

#Reddit API function calls

def leagueoflegends():
    #search for posts in lol sub
    
    submission = redditObj.get_subreddit('leagueoflegends')

    for submission in submission.get_hot(limit=15):
        if is_score(submission.url, submission.title):
            tweet_post(submission.title, submission.url, submission.id)
    time.sleep(1800)


def tweet_post(title, url, subid):
   
    #post found scores to twitter
    CONSUMERKEY = keys[0]
    CONSUMERSECRET = keys[1]
    ACCESSKEY = keys[2]
    ACCESSSECRET = keys[3]
    
    nonDuplicateFlag = True
    
    auth = tweepy.OAuthHandler(CONSUMERKEY, CONSUMERSECRET)
    auth.set_access_token(ACCESSKEY, ACCESSSECRET)
    api = tweepy.API(auth)

    #Clean link to prepare for tweeting
    title = tweet_cleanup(title)
   
    shortener = Shortener('TinyurlShortener')
    tinyurl = shortener.short(url)
    tweet = tweet_cleanup(title)
   
    if subid in postedTweets:
        nonDuplicateFlag = False
        return
    
    post = title + tinyurl

    try:
        api.update_status(post) #post the tweet
    except:
        print('Tweet not posted. Check Issue. Length= ', len(post))
        return

    postedTweets.append(subid)
    update_db()

#helper functions

def tweet_cleanup(twit):
    #delete unnecessary ( )
    twit = re.sub('[[](){}<>]', '', twit)
    
    #delete unnecessary -
    twit = re.sub('-', ' ', twit)
    
    #delete unessecary /
    twit = re.sub('/', '', twit)
    
    #delete spoiler
    twit = re.sub('Spoiler', '', twit)
    
    #delete post-match discussion text
    twit = re.sub(' Post Match Discussion', '', twit)
    
    #shorten vs.
    twit = re.sub('vs.', 'v', twit)
    
    #because some people are stupid
    twit = re.sub('(self.leagueoflegends)', '', twit)

    #shorten league names
    twit = re.sub(' Champions Spring', '', twit)
    twit = re.sub(' Summer Split', '', twit)
    twit = re.sub('2016 ', '', twit)
    twit = re.sub('Spring', '', twit)
    twit = re.sub('Week', 'Wk', twit)
    twit = re.sub('LCS', '', twit)
    
    #shorten NA team names
    twit = re.sub('Counter Logic Gaming', 'CLG', twit)
    twit = re.sub('Echo Fox', 'FOX', twit)
    twit = re.sub('Team Impulse', 'IMP', twit)
    twit = re.sub('Team Liquid', 'LQD', twit)
    twit = re.sub('Team Solomid', 'TSM', twit)
    twit = re.sub('Team Dignitas', 'DIG', twit)
    twit = re.sub('Renegades', 'RNG', twit)
    twit = re.sub('Cloud9', 'C9', twit)
    twit = re.sub('Immortals', 'IMR', twit)
    twit = re.sub('NRG eSports', 'NRG', twit)

    #shorten EU team names
    twit = re.sub('Fnatic', 'FNC', twit)
    twit = re.sub('G2 Esports', 'G2', twit)
    twit = re.sub('H2K Gaming', 'H2K', twit)
    twit = re.sub('Roccat', 'ROC', twit)
    twit = re.sub('Unicorns of Love', 'UOL', twit)
    twit = re.sub('Elements', 'ELM', twit)
    twit = re.sub('Giants', 'GIA', twit)
    twit = re.sub('Origen', 'ORG', twit)
    twit = re.sub('Splyce', 'SPL', twit)
    twit = re.sub('Vitality', 'VIT', twit)

    #shorten LCK team names
    twit = re.sub('KT Rolster', 'KT', twit)
    twit = re.sub('Longzhu Gaming', 'LOG', twit)
    twit = re.sub('Samsung Galaxy', 'SMG', twit)
    twit = re.sub('SK Telecom T1', 'SKT', twit)
    twit = re.sub('ROX Tigers', 'TIG', twit)
    twit = re.sub('e-mFire', 'EMF', twit)
    twit = re.sub('Jin Air Green Wings', 'JAG', twit)
    twit = re.sub('Afreeca Freecs', 'AFR', twit)
    twit = re.sub('SBENU Sonicboom', 'SBN', twit)
    twit = re.sub('CJ Entus', 'CJE', twit)

    #shorten LPL team names
    twit = re.sub('EDward Gaming', 'EDG', twit)
    twit = re.sub('Energy Pacemaker', 'EPA', twit)
    twit = re.sub('EP.A', 'EPA', twit)
    twit = re.sub('HY Gaming', 'HYG', twit)
    twit = re.sub('Hyper Youth Gaming', 'HYG', twit)
    twit = re.sub('Invictus Gaming', 'IG', twit)
    twit = re.sub('LGD Gaming', 'LGD', twit)
    twit = re.sub('Masters 3', 'M3', twit)
    twit = re.sub('Oh My God', 'OMG', twit)
    twit = re.sub('Qiao Gu Reapers', 'QG', twit)
    twit = re.sub('Snake Esports', 'SNK', twit)
    twit = re.sub('Snake', 'SNK', twit)
    twit = re.sub('Team WE', 'WE', twit)
    twit = re.sub('Vici Gaming', 'VG', twit)

    #shorten LMS team names
    twit = re.sub('AHQ eSports Club', 'AHQ', twit)
    twit = re.sub('Flash Wolves', 'FLW', twit)
    twit = re.sub('Hong Kong Esports', 'HKE', twit)
    twit = re.sub('Mignight Sun Esports', 'MSE', twit)
    twit = re.sub('Taipei Assassins', 'TPA', twit)
    twit = re.sub('Machi E-sports', 'MAE', twit)
    twit = re.sub('Cougar E-Sport', 'CGR', twit)
    twit = re.sub('eXtrame Gamers', 'EXT', twit)

    #get rid of double spaces
    twit = re.sub('  ', ' ', twit)
    
    #get rid of brackets
    twit = re.sub('\[\]', '', twit)
    
    return twit

def is_score(url, title):
    #check if the post is a score
    #if('self' in url):
    if 'Post-Match Discussion' in title:
        return True
    else:
        return False

#Main function
def init_db():
    #init post array
    global postedTweets

    try:
        with open('posts.DAT', 'rb') as fileRead:
            postedTweets = pickle.load(fileRead)
    except:
        print('no prev posts found')
        return

def update_db():
    #dump posted tweets to array
    global postedTweets
    
    with open('posts.DAT', 'wb+') as fileWrite:
        pickle.dump(postedTweets, fileWrite)

if __name__ == "__main__":
    init_db()
    leagueoflegends()

