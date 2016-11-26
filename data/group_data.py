import json
from datetime import datetime
from datetime import timedelta

def translate_time(timestr):
    d = datetime.strptime(timestr, "%Y-%m-%d %H:%M") # PST
    d = d + timedelta(hours=3) # ET
    return d.strftime("%Y/%m/%d")


tweet_folder = 'tweets/history_data/'
stock_folder = 'stock/two years/'

# Set file pairs
company_configs = [
    {
        'name': 'VA',
        'sentiment_file': 'sentiment_virgin_america.txt-maxEnt20000',
        'stock_file': 'VA.csv'
    },
    {
        'name': 'UAL',
        'sentiment_file': 'sentiment_united.txt-maxEnt20000',
        'stock_file': 'UAL.csv'
    },
    {
        'name': 'LUV',
        'sentiment_file': 'sentiment_southwest_air.txt-maxEnt20000',
        'stock_file': 'LUV.csv'
    },
    {
        'name': 'DAL',
        'sentiment_file': 'sentiment_jet_blue.txt-maxEnt20000',
        'stock_file': 'DAL.csv'
    },
    {
        'name': 'AAL',
        'sentiment_file': 'sentiment_america_airline.txt-maxEnt20000',
        'stock_file': 'AAL.csv'
    },
    {
        'name': 'AAPL',
        'sentiment_file': 'sentiment_apple.txt-maxEnt20000',
        'stock_file': 'AAPL.csv'
    },
]

# read and match, group stock and tweet data by date


# Output format: a list of dict
# [{"date": 2016/11/26, "stock": 45.4, "tweets":[0.5,0.6,0.4,0.2,0.9,0.2]}, {"date": ..., "stock": ..., "tweets": ...} ]

for company in company_configs:
    dict = {}
    
    with open(stock_folder + company['stock_file'], 'r') as f_stock:    
        lines = f_stock.readlines()
        for i in range(2, len(lines)):
            attrs = lines[i].split(",")
            date = attrs[0][1:-1]
            
            if date < '2015/12/18':
                continue

            close_val = float(attrs[1][1:-1])
            dict[date] = {}
            dict[date]["date"] = date
            dict[date]["stock"]  = close_val
            dict[date]["tweets"] = []

    with open(tweet_folder + company['sentiment_file'], 'r') as f_tweets:
        sentiments = json.loads(f_tweets.read())
        for tweet in sentiments:
            date = translate_time(tweet['time'])
            
            if date not in dict:
                continue

            senti = tweet['polarity']
            dict[date]["tweets"].append(senti)
    
    with open(company['name'] + '_stock_tweet', 'w') as f_output:
        output = []
        for k, v in sorted(dict.items()):
            output.append(v)
        f_output.write(json.dumps(output))
