from twython import Twython
import twython

from TwitterZuil.twitter_auth import (
    CONSUMER_KEY,
    CONSUMER_KEY_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

twitter = Twython(
    CONSUMER_KEY,
    CONSUMER_KEY_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)


def tweet_message(msg):
    try:
        params = twitter.update_status(status=msg)
        return params['id']
    except twython.exceptions.TwythonError:
        return None


