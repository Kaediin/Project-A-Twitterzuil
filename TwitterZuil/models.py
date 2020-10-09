from django.db import models


# Create your models here.
class Tweet:

    def __init__(self, id, text, username, datetime, is_reviewed, is_tweeted, twitter_tweet_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.text = text
        self.username = username
        self.datetime = datetime
        self.is_reviewed = is_reviewed
        self.is_tweeted = is_tweeted
        self.twitter_tweet_id = twitter_tweet_id


class Moderator:

    def __init__(self, id, fullname, first_name, infix, last_name, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.fullname = fullname
        self.first_name = first_name
        self.infix = infix
        self.last_name = last_name
        self.password = password


class Scherm:

    def __init__(self, id, locatie, naam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.locatie = locatie
        self.naam = naam


class Weer:
    def __init__(self, conditie, temp, icon, wind_directie, wind_kmph, mm_regen, gevoelstemp, uv, regio, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conditie = conditie
        self.temp = temp
        self.icon = icon
        self.wind_directie = wind_directie
        self.wind_kmph = wind_kmph
        self.mm_regen = mm_regen
        self.gevoelstemp = gevoelstemp
        self.uv = uv
        self.regio = regio