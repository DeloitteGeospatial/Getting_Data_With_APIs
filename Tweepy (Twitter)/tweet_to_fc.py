import arcpy
print "arcpy imported\n"
import json

f = open(r"C:\Users\johtran\Desktop\My Docs\Projects\Hackathon_Tampa\20160113 - Howell_Hackathon data\Working\tweepy_data.json", "r")
fc = r"C:\Users\johtran\Desktop\My Docs\Projects\Hackathon_Tampa\20160113 - Howell_Hackathon data\Working\Tweets.gdb\Tweets"
cursor = arcpy.da.InsertCursor(fc, ["SHAPE@XY", "Text", "Source", "Hashtags", "X", "Y"])

for line in f:
    tweet = json.loads(line)
    text = tweet["text"]
    source = tweet["source"]
    hashtags = ", ".join(["#"+h["text"] for h in tweet["entities"]["hashtags"]])
    lat, lon = tweet["geo"]["coordinates"]
    cursor.insertRow(((lon,lat), text, source, hashtags, lon, lat))

f.close()
del cursor
