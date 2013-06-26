# tweet_sentiment.py
# Author: Rahul Ravindran - 2013

import sys
import json

scores = {}
tweets = []



def build_dict(file):
    for line in file:
        term, score = line.split("\t")
        scores[term] = int(score)

def tweet_rating(line):
    words = line.split(" ")
    score = 0
    for word in words:
        if word in scores:
            score = score + scores[word]
    return score

def get_tweet_text(file):
    for line in file:
        data = json.loads(line)
        if len(data) > 10:
	     tweets.append(data['text'])

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
#    lines(sent_file)
#    lines(tweet_file)
    build_dict(sent_file)
    get_tweet_text(tweet_file)
#    print len(tweets)
    for line in tweets:
         print tweet_rating(line)
if __name__ == '__main__':
    main()
