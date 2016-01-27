import json

with open(r"C:\Users\johtran\Desktop\My Docs\Projects\Hackathon_Tampa\20160113 - Howell_Hackathon data\Working\tweepy_data.json", "r") as tweets:
    for line in tweets:
        tweet = json.loads(line)
        print u"Text: {0}".format(tweet["text"])
        print u"Source: {0}".format(tweet["source"])
        print u"Geo: {0}".format(tweet["geo"])
        print u"Place: {0}".format(tweet["place"])
        hashtags = [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]]
        if hashtags:
            print u"Hashtags: #{0}".format(", #".join(hashtags))
        else:
            print u"Hashtags: "
        print "\n"
