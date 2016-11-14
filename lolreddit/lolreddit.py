import re
import requests
import praw
import peewee

def get_spells(id, base, key):
    champ = 'static-data/NA/v1.2/champion/'
    spells = '?champData=spells'
    url = base+champ+id+spells+key
    print(url)
    request = requests.get(url)
    request = request.json()
    print(request['spells'][0]['name'])
    print(request['spells'][0]['key'])
    print(request['spells'][0]['costBurn'])
    print(request['spells'][0]['cooldownBurn'])
    print(request['spells'][0]['vars'][0]['coeff'])
    print(request['spells'][0]['sanitizedTooltip'])
    print(request['spells'][0]['effect'][1])


def get_champions(base,key):
    


def build():
    key = '&api_key=462d0d85-d692-4af5-b91f-4ed9cf0b2efe'
    base = 'https://na.api.pvp.net/api/lol/'
    get_spells('103', base, key)


def main():
    build()


main()


def login():
    '''login to reddit using praw'''
    keys = []
    with open('lily/info/keys.txt') as file:
        keys = file.readlines()
    reddit = praw.Reddit('lily')
    reddit.login(keys[0].strip(), keys[1].strip(), disable_warning=True)
    return reddit


def parse(comment, regex):
    '''TODO create function'''

    sr = re.search(regex, comment)
    found = [x[1:-1] for x in found.groups()]

    return found

def get_requests(regex, db):
    search = parse(comment, regex)
    to_reply = []
    for i in search:
        for j in db:
            if i == j.name:
                to_reply.append(j.field)


def listen():
    reddit = helpers.login()

    subreddit = 'leagueoflegends'
    cre = re.compile(r"\[([a-z0-9]+)\]")
    sre = re.compile(r"\[([a-z0-9]+\s-\s[pqwer])\]")
    ire = re.compile(r"\[([a-z0-9\ ]+)\]")
    regexes = [cre, sre, ire]

    cdb = Champion.get()
    sdb = Skill.get()
    idb = Item.get()
    dbs = [cdb, sdb, idb]

    response = ''
    end = '\nSee more at github.com'

    for comment in praw.helpers.comment_stream(reddit, subreddit):
        for r, d in zip(regexes, dbs):
            to_reply = get_requests(r, d)
            for t in to_reply:
                response += t
        if response:
            response += end
            # reply to the comment from the stream