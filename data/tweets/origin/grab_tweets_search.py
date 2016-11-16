import tweepy
import os
import sys
import jsonpickle
import warnings
import time
import logging

logging.basicConfig()
warnings.filterwarnings("ignore")

class Tweet():
    def __init__(self, tweet):
        self.id = tweet.id
        self.user_name = tweet.user.name
        self.screen_name = tweet.user.screen_name
        self.text = tweet.text
        self.created_at = tweet.created_at 
        self.favorite_count = tweet.favorite_count
        if hasattr(tweet, 'retweeted_status'):
            self.retweet_id = tweet.retweeted_status.id
            self.retweet_count = tweet.retweeted_status.retweet_count

def grab_tweets_by_keyword(keyword):
    count_per_query = 100 # the max number allowed
    print 'Searching keyword:', keyword
    # create folder if needed
    if not os.path.exists(keyword):
        os.makedirs(keyword)

    since_id = -1
    max_id = -1
    # get the maxId in the past and set it as sinceID
    for root, dirs, files in os.walk(keyword):
        for file in files:
            if file.endswith(".txt"):
                try:
                    since_id = max(since_id, int(file[0:-4],10))
                except:
                    pass

    download_cnt = 0
    while(True):
        try:
            if since_id == -1:
                if max_id == -1:
                    tweets = api.search(q=keyword, count=count_per_query, lang='en')
                else:
                    tweets = api.search(q=keyword, count=count_per_query, lang='en', max_id = max_id)
            else:
                if max_id == -1:
                    tweets = api.search(q=keyword, count=count_per_query, lang='en', since_id = since_id)
                else:
                    tweets = api.search(q=keyword, count=count_per_query, lang='en', since_id = since_id, max_id = max_id)
     
            if not tweets:
                print '\t no more tweets'
                break
            
            max_id = tweets[-1].id - 1

            print("\t Downloaded {0} tweets,\t{1} ~ {2}".format( len(tweets) , tweets[0].created_at, tweets[-1].created_at ) )
            download_cnt += len(tweets)

            f = open( keyword + '/' + str(tweets[0].id) +'.txt','w')
            for tweet in tweets:
                f.write(jsonpickle.encode(Tweet(tweet), unpicklable=False)+'\n')
            f.close()
            
        except tweepy.TweepError as e:
            print "\t some error : " + str(e) + ' we need to wait'
            time.sleep(60 * 15 + 30) # wait for 15 minutes and 30 seconds

    print keyword + ': altogether ' + str(download_cnt) + ' tweets'

if __name__ == "__main__":
    auth = tweepy.AppAuthHandler('XOHqIQzn8hXXm7Tvx9a1ucwHb', 'K0DGwJL78ItQnL3Z5mqtPLXN1y0bJg7LSo2wmyktXdi8B1GaFo')
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if (not api):
        print "Can't authenticate"
        sys.exit(-1)

    keywords = ['@JetBlue OR #JetBlue', 
                '@VirginAmerica OR #VirginAmerica', 
                '@SouthwestAir OR #SouthwestAir', 
                '@Apple OR #AAPL', 
                '@united',
                '@AmericanAir OR #AmericanAir']
    for keyword in keywords:
        grab_tweets_by_keyword(keyword)