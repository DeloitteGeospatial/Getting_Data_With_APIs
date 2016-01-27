import tweepy
import os
import json

# Consumer keys and access tokens used for OAUTH
consumer_key = "KMtKN5XHNiDxCI5s6ELv5vGXF"
consumer_secret = "T0T4fXCx64i8Oh5wtHF4DVeZ2cFDTJKqZc6YS2ueDGNYq8ZY4u"
access_token = "4830201730-5ubQe0muCHtC8TuIsH9OrQVeHIcpCajIKdITqlf"
access_secret = "GXWcWdwpkBQcLhVGdxqQlWm2MJG9InXxz4YyublbrcviL"
access_level = "Read and write"
owner = "johnkntran"
owner_id = "4830201730"

class StdOutListener(tweepy.streaming.StreamListener):
    def __init__(self):
        self.numtweet = 0
    def on_data(self, data):
        with open(r"C:\Users\johtran\Desktop\My Docs\Projects\Hackathon_Tampa\20160113 - Howell_Hackathon data\Working\tweepy_data.json", "a") as f:
            tweet = json.loads(data)
            try:
                if tweet["geo"]:
                    f.write(data)
                    text = unicode(tweet["text"])
                    lon, lat = tweet["geo"]['coordinates']
                    print u"Tweet #{0} {1}; coords = ({2}, {3})\n".format(self.numtweet, text, lat, lon)
                    if self.numtweet >= 100:
                        os._exit(0)
                    self.numtweet += 1
            except KeyError:
                pass
    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = tweepy.Stream(auth, l)
    stream.filter(track=["winter", "storm", "snow"], async=True)
