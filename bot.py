import tweepy
import pandas as pd

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")


consumer_key = 'hQPh8DurzbBLNfudONerRPM9r'
consumer_secret = 'dRemA54f0FiNG6ra4iULV5jzBSCppcWAkQ25OKcnjG11PUVwWP'
access_token = '1264432304295944192-ADLGhXgrV7BTqn1N0cgtWKgxg1d4F6'
access_token_secret = 'eBnp64F7HDXUf0qqLbAynKaloUlyzmT9bEbepbJjFpCgJ'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["Python", "Django", "Tweepy"], languages=["en"])

