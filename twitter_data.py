"""
This module is gathering and storing data from twitters to the right folder candidate.
"""

import tweepy
import os
import re

def get_auth() -> object:
    """
    function to obtain credentials

    :return: Twitter API credentials
    """
    # PROD MOD
    if os.environ.get("ENV") == "PROD":
        consumer_key = os.environ.get("CONSUMER_KEY")
        consumer_secret = os.environ.get("CONSUMER_SECRET")
        access_token = os.environ.get("ACCESS_TOKEN")
        access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

    # TEST MOD
    else:
        all_keys = open("twitterauth", "r").read().splitlines()
        auth = tweepy.OAuthHandler(all_keys[0], all_keys[1])
        auth.set_access_token(all_keys[2], all_keys[3])

    api = tweepy.API(auth)

    return api

def get_cleaned(msg : str) -> str:
    """
    This function use regex function to clean up a message.

    :param: The given message (string)
    :return: cleaned message (string)
    """
    # remove # and @
    msg = re.sub("@[A-Za-z0-9_]+", "", msg)
    msg = msg.replace('#', '')

    # Remove urls
    msg = re.sub(r"http\S+", "", msg)

    # Symbols & pics & emoji
    EMOJI_PATTERN = re.compile(
        "(["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "])"
    )
    msg = re.sub(EMOJI_PATTERN, '', msg)

    return msg

def get_tweets(api: object, account: str) -> list:
    """
    This function is extracting the last n'th tweets from a given account candidate.

    :param api: api credentials from tweepy.
    :param account: account to search for.
    :return tweet_text: list of tweets.
    """

    # Get tweets from API
    tweets = tweepy.Cursor(api.user_timeline, id=account, tweet_mode='extended').items(50)
    tweet_text = [tweet.full_text for tweet in tweets]

    return tweet_text

def save_tweets(name, tweet_text):
    """
    This function is saving the tweet list on .txt file on the given folders candidate.

    :param name: Name of the candidate.
    :param tweet_text: list of tweets.
    :return:
    """

    # Saving file
    path = os.path.join("./files", name, "twitter.txt")
    with open(path, 'w') as f:
        f.write("\n".join(tweet_text))

def twitter_main(name):
    """
    This is the main function of this module.

    :param name: Name of the candidate.
    :return:
    """

    # Twitter account correspondance
    d_twitter = {
        "Macron": "@EmmanuelMacron",
        "Lepen": "@MLP_officiel"
    }

    api = get_auth()
    tweet_text = get_tweets(api, d_twitter[name])
    tweet_text = [get_cleaned(tweet) for tweet in tweet_text]
    save_tweets(name, tweet_text)
