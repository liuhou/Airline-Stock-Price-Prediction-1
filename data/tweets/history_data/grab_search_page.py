import os
import requests
import datetime
import time
import codecs
import re
import json
from bs4 import BeautifulSoup
import warnings
import logging
logging.basicConfig()
warnings.filterwarnings("ignore")



def build_params(query_word, start_time, end_time, max_position):
    params = {
        'vertical':'default', 
        'include_available_features':1, 
        'include_entities':1, 
        'src':'typd', 
        'reset_error_state':0,
        'q': "{0} lang:en since:{1} until:{2} include:retweets".format(query_word, start_time, end_time),
        'max_position': max_position
    }
    return params

timeline_url = 'https://twitter.com/i/search/timeline'

# Notes: if grabbing stops ahead of time, 
# 1. change token
# 2. change header
# 3. subtract min_position

#headers might also change
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def request_result(params):
    global timeline_url
    global headers
    
    res_json = None
    
    while(True):
        try:
            res = requests.get(timeline_url, params=params, headers=headers)
            # res = requests.get(tmp, headers=headers)
            res_json = res.json()
            break
        except:
            time.sleep(60) 

    return res_json

def write_result(query_word, res_json):
    soup = BeautifulSoup(res_json['items_html'])
    tweets = soup.find_all( id = re.compile('stream-item-tweet') )
    
    if len(tweets) == 0:
        return False

    file = codecs.open(query_word + '/' + res_json['min_position'][0:43]+".dat", "w", "utf-8")
    time = 0
    for i in range(0, len(tweets)):
        try:
            text = tweets[i].find("p", {"class":'tweet-text'}).text
            timestamp = tweets[i].find("small", {"class":"time"}).span['data-time']
            user_name = tweets[i].find("span", {"class":"username"}).text
            tweet_id = tweets[i]['data-item-id']
            time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')
            file.write(
                json.dumps( {
                        "id":tweet_id, 
                        "text": text, 
                        "timestamp":timestamp, 
                        "name": user_name, 
                        "time": time
                    } ) + "\n")
        except:
            print 'error with ' + str(i)
    print "\n" + str( len(tweets)) + " tweets --> " + str(time),
    file.close()
    return True


if __name__ == "__main__":
    start_time = '2015-11-19'
    end_time   = '2016-11-19'
    keywords = [ #'@JetBlue OR #JetBlue', 
                 #'@VirginAmerica OR #VirginAmerica', 
                 #'@SouthwestAir OR #SouthwestAir', 
                 #'@united',
                 '@AmericanAir OR #AmericanAir',
                 #'@Apple OR #AAPL'
                ]
    

    # query_word = '@JetBlue OR #JetBlue'
    for query_word in keywords:
        print "\ngrabbing keyword: " + query_word
        min_id = 900000000000000000
        if not os.path.exists(query_word):
            os.makedirs(query_word)
        for root, dirs, files in os.walk(query_word):
            for file in files:
                if file.endswith(".dat"):
                    try:
                        min_id = min(min_id, int(file[6:24]))
                    except:
                        pass
        
        
        # the token will change every day
        token = "BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAIAAAAAACAAAAAAAAAAQAAAgAAAACAAAAEAAAAQAAAQAAAAAAAAAAAIAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAQgAAAAAAIAAAAAAAAAGACAgAAAAAAAAAAAAAAAgAAAAAAAAQAAAiAAAAAEAAAAAAAABAAAAAABAAAAEAAAAAABAAAAAAAAAAAAAA"
    

        # we need to pass the minimal_tweet_id as the "max_position" parameter
        # so that incoming tweets will have a id smaller than that    
        
        res_json = {'min_position': "TWEET-{0}-900000000000000000-".format(min_id) + token}
        empty_cnt = 0
        while(True):
            res_json = request_result(build_params(query_word, start_time, end_time, res_json['min_position']))
            has_more_items = write_result(query_word, res_json)
            if not has_more_items: # when result is empty, we try subtracting the min id for ten times
                empty_cnt += 1
                print 'we got empty result for ' + str(empty_cnt) + ' times'
                if empty_cnt == 10:
                    break
                
                min_id = int(res_json['min_position'][6:24]) - 10000000000000L
                res_json['min_position'] = res_json['min_position'][0:6] + str(min_id) + res_json['min_position'][24:]
            else:
                empty_cnt = 0

        print "\nThe end for keyword: " + query_word