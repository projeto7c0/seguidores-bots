import tweepy
import json


def authenticate_v2(bearer_token = None):
        # client = tweepy.Client(bearer_token=tt_config['bearer_token'], access_token=tt_config['access_token'], access_token_secret=tt_config['access_token_secret'], consumer_key=tt_config['api_key'], consumer_secret=tt_config['api_secret_key'])
        if (bearer_token): 
            client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        else:
            with open("seguidores_politicos/config.json") as jsonfile:
                tt_config = json.load(jsonfile)['twitter-keys']

            client = tweepy.Client(bearer_token=tt_config['bearer_token'], wait_on_rate_limit=True)

        return client


def authenticate_v1(bearer_token):
        # client = tweepy.Client(bearer_token=tt_config['bearer_token'], access_token=tt_config['access_token'], access_token_secret=tt_config['access_token_secret'], consumer_key=tt_config['api_key'], consumer_secret=tt_config['api_secret_key'])
        
        auth = tweepy.OAuth2BearerHandler(bearer_token)
        api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=5, retry_delay=30)

        return api
