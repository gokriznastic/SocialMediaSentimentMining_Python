import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Setting up authentication with twitter
consumer_key = 'MTVOKJ3Kzn4hmpefMxZyeD1EU'
consumer_secret = 'SMCduI3tChYi3oda4xg9vH1VidQU1oaL4dZ9gKt8gx985N7PpG'
access_token = '3310773140-N3oAdYWWQKhN1OI1GNEIBSoE0UfnMLVOvaWLmDn'
access_secret = 'mF6FaJ5SxEtLr1nySc9TdrVDLYCbDKrnEbACPmoUKlhKk'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# We'll be storing tweets in JSON Lines format instead
# Each line of the file is a valid JSON document so it is easier to manipulate


# method to read your own home timeline (limited to 800 tweets by Twitter)
def home_timeline():
    print("FETCHING TWEETS FROM YOUR HOME TIMELINE. THIS MAY TAKE SOME TIME >>>>>")
    fname = 'tweetdata.jsonl'
    with open(fname, 'w') as f:
        for page in tweepy.Cursor(api.home_timeline, count=200).pages(4):
            for status in page:
                f.write(json.dumps(status._json)+"\n")


# method to read your a specific users timeline (limited to 3200 tweets by Twitter)
def user_timeline(user):
    print("FETCHING TWEETS FROM ", user, " TIMELINE. THIS MAY TAKE SOME TIME >>>>>")
    fname = 'tweetdata.jsonl'
    with open(fname.format(user), 'w') as f:
        for page in tweepy.Cursor(api.user_timeline, screen_name=user, count=200).pages(16):
            for status in page:
                f.write(json.dumps(status._json)+"\n")


# method to stream tweets from twitter using hashtags
def stream_by_hashtag(hash_search):
    print("STREAMING TWEETS HAVING ->", hash_search)
    print("STOP THE PROGRAM EXECUTION WHEN YOU WANT TO STOP THE STREAMING >>>>>")
    fname = 'tweetdata.jsonl'

    class MyListener(StreamListener):

        def on_data(self, data):
            try:
                with open(fname, 'a') as f:
                    f.write(data)
                    return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
            return True

        def on_error(self, status):
            print(status)
            return True

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=[hash_search])


# method to allow user to stream tweets from any of the above three sources according to their choice
def choice(x):
    if x == 'a' or x == 'A':
        home_timeline()
    elif x == 'b' or x == 'B':
        print("INPUT THE TWITTER HANDLE WITHOUT @ >>>>>")
        username = input()
        user_timeline(username)
    elif x == 'c' or x == 'C':
        print("INPUT THE HASHTAG OF THE TWEETS YOU WANT TO STREAM (WITH #) >>>>>")
        hash_term = input()
        stream_by_hashtag(hash_term)
    else:
        print("error in choice")


# Now we allow user to select from where does they want to collect the tweets
print("THE TWEETS CAN BE FETCHED VIA THREE SOURCES >>>>>")
print("a - your own HOME TIMELINE")
print("b - another USER'S TIMELINE")
print("c - live streamed USING HASHTAGS")
print("GO AHEAD, ENTER YOUR CHOICE >>>>>")
user_input = input()
choice(user_input)
