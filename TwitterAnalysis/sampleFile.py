# sampleFile.py 
# Author:Rahul Ravindran 2013

import urllib
import json

response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft")
tweets = json.load(response)
tweetCounts = tweets['results']
for i in tweetCounts:
    print i[u'text']

