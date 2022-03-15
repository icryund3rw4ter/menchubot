import random
import re
import sys
import twitter
import markov
from bs4 import BeautifulSoup

# Python 3
from html.entities import name2codepoint as n2c
from urllib.request import urlopen
from local_settings import *


def connect(type='twitter'):
    if type == 'twitter':
        return twitter.Api(consumer_key=MY_CONSUMER_KEY,
                       consumer_secret=MY_CONSUMER_SECRET,
                       access_token_key=MY_ACCESS_TOKEN_KEY,
                       access_token_secret=MY_ACCESS_TOKEN_SECRET,
                       tweet_mode='extended')
    return None


def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return chr(int(text[3:-1], 16))
            else:
                return chr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        if guess == "apos":
            guess = "lsquo"
        numero = n2c[guess]
        try:
            text = chr(numero)
        except KeyError:
            pass
    return text


def filter_status(text):
    text = re.sub(r'\b(RT|MT) .+', '', text)  # take out anything after RT or MT
    text = re.sub(r'(\#|@|(h\/t)|(http))\S+', '', text)  # Take out URLs, hashtags, hts, etc.
    text = re.sub('\s+', ' ', text)  # collaspse consecutive whitespace to single spaces.
    text = re.sub(r'\"|\(|\)', '', text)  # take out quotes.
    text = re.sub(r'\s+\(?(via|says)\s@\w+\)?', '', text)  # remove attribution
    text = re.sub(r'<[^>]*>','', text) #strip out html tags from mastodon posts
    htmlsents = re.findall(r'&\w+;', text)
    for item in htmlsents:
        text = text.replace(item, entity(item))
    text = re.sub(r'\xe9', 'e', text)  # take out accented e
    return text


def grab_tweets(api, max_id=None):
    source_tweets = []
    user_tweets = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=True)
    if user_tweets:
        max_id = user_tweets[-1].id - 1
        for tweet in user_tweets:
            if tweet.full_text:
                tweet.text = filter_status(tweet.full_text)
            else:
                tweet.text = filter_status(tweet.full_text)
            if re.search(SOURCE_EXCLUDE, tweet.text):
                continue
            if tweet.text:
                source_tweets.append(tweet.text)
    else:
        pass
    return source_tweets, max_id

def grab_toots(api, account_id=None,max_id=None):
    if account_id:
        source_toots = []
        user_toots = api.account_statuses(account_id)
        max_id = user_toots[len(user_toots)-1]['id']-1
        for toot in user_toots:
            if toot['in_reply_to_id'] or toot['reblog']:
                pass #skip this one
            else:
                toot['content'] = filter_status(toot['content'])
                if len(toot['content']) != 0:
                    source_toots.append(toot['content'])
        return source_toots, max_id

if __name__ == "__main__":
    order, guess = ORDER, 0

    api = connect()         
    source_statuses = []
    if STATIC_TEST:
        file = TEST_SOURCE
        print(">>> Generating from {0}".format(file))
        string_list = open(file).readlines()
        for item in string_list:
            source_statuses += item.split(",")
    if ENABLE_TWITTER_SOURCES and TWITTER_SOURCE_ACCOUNTS and len(TWITTER_SOURCE_ACCOUNTS[0]) > 0:
        twitter_tweets = []
        for handle in TWITTER_SOURCE_ACCOUNTS:
            user = handle
            handle_stats = api.GetUser(screen_name=user)
            status_count = handle_stats.statuses_count
            max_id, my_range = None, min(17,  int((status_count/200) + 1))
            for x in range(1, my_range):
                twitter_tweets_iter, max_id = grab_tweets(api, max_id)
                twitter_tweets += twitter_tweets_iter
                
            #print("{0} tweets found in {1}".format(len(twitter_tweets), handle))
            if not twitter_tweets:
                print("Error fetching tweets from Twitter. Aborting.")
                sys.exit()
            else:   
                source_statuses += twitter_tweets
                
        if len(source_statuses) == 0:
            print("No statuses found!")
            sys.exit()
        mine = markov.MarkovChainer(order)
        for status in source_statuses:
            if not re.search('([\.\!\?\"\']$)', status):
                status += "."
            mine.add_text(status)
        for x in range(0, 10):
            ebook_status = mine.generate_sentence()

        # randomly drop the last word, as Horse_ebooks appears to do.
        if random.randint(0, 4) == 0 and re.search(r'(in|to|from|for|with|by|our|of|your|around|under|beyond)\s\w+$', ebook_status) is not None:
            print("Losing last word randomly")
            ebook_status = re.sub(r'\s\w+.$', '', ebook_status)
            print(ebook_status)

        # if a tweet is very short, this will randomly add a second sentence to it.
        if ebook_status is not None and len(ebook_status) < 40:
            rando = random.randint(0, 10)
            if rando == 0 or rando == 7:
                print("Short tweet. Adding another sentence randomly")
                newer_status = mine.generate_sentence()
                if newer_status is not None:
                    ebook_status += " " + mine.generate_sentence()
                else:
                    ebook_status = ebook_status
            elif rando == 1:
                # say something crazy/prophetic in all caps
                print("ALL THE THINGS")
                ebook_status = ebook_status.upper()

        # throw out tweets that match anything from the source account.
        if ebook_status is not None and len(ebook_status) < 210:
            for status in source_statuses:
                if ebook_status[:-1] not in status:
                    continue
                else:
                    print("TOO SIMILAR: " + ebook_status)
                    os.execv(__file__, [__file__] + sys.argv)

            if not DEBUG:
                if ENABLE_TWITTER_POSTING:
                    status = api.PostUpdate(ebook_status)
            print(ebook_status)

        elif not ebook_status:
            print("Status is empty, sorry.")
        else:
            print("TOO LONG: " + ebook_status)
