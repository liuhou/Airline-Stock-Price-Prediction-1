
import csv
from src import classifier

class KaggleEntry:
    """represent an entry in the kaggle dataset."""
    def __init__(self, sentiment, confidence, text):
        self.sentiment = sentiment
        self.confidence = confidence
        self.text = text


def categorize(happiness, thres1, thres2):
    if happiness < 0:
        return "unkown"
    elif happiness > thres2:
        return "positive"
    elif happiness < thres1:
        return "negative"
    else:
        return "neutral"

def KaggleVerify(fn, classifier):
    cnt = 0
    correct = 0
    with open(fn) as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            cnt += 1
            if cnt > 1:
                entry = KaggleEntry(line[1], line[2], line[10])
                happiness = classifier.classify(entry.text)
                if categorize(happiness, 3.0, 7.0) == entry.sentiment:
                    correct += 1
    cnt -= 1
    print "cnt ", cnt, " correct ", correct, " ", correct / (cnt * 1.0)

def KaggleVerifyBinary(fn, classifier):
    lines = 0
    cnt = 0
    correct = 0
    with open(fn) as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            lines += 1
            if lines > 1:
                entry = KaggleEntry(line[1], line[2], line[10])
                if entry.sentiment == "positive" or entry.sentiment == "negative":
                    cnt += 1
                    happiness = classifier.classify(entry.text)
                    if categorize(happiness, 4.9, 5.1) == entry.sentiment:
                        correct += 1
    print "cnt ", cnt, " correct ", correct, " ", correct / (cnt * 1.0)

def GoldVerifyBinary(fn, classifier):
    lines = 0
    cnt = 0
    correct = 0
    with open(fn) as f:
        for line in f:
            lines += 1
            sentiment, text = line.split('\t')
            entry = KaggleEntry(sentiment, 1, text)
            if entry.sentiment == "positive" or entry.sentiment == "negative":
                cnt += 1
                happiness = classifier.classify(entry.text)
                if categorize(happiness, 4.9, 5.1) == entry.sentiment:
                    correct += 1

    print "cnt ", cnt, " correct ", correct, " ", correct / (cnt * 1.0)


if __name__ == "__main__":
    classifier = classifier.NaiveClassifier("../data/labMIT.txt")
    KaggleVerify("twitter-airline-sentiment/Tweets.csv", classifier)
    KaggleVerifyBinary("twitter-airline-sentiment/Tweets.csv", classifier)
    GoldVerifyBinary("twitter-airline-sentiment/A.tsv", classifier)
    GoldVerifyBinary("twitter-airline-sentiment/B.tsv", classifier)
    classifier.showReason("Wow Vick this is why i stopped with montreal canadiens..foreign languages..say one thing..may mean  http://t.co/bZ1xEP8J")
    print classifier.classify("Wow Vick this is why i stopped with montreal canadiens..foreign languages..say one thing..may mean  http://t.co/bZ1xEP8J")
