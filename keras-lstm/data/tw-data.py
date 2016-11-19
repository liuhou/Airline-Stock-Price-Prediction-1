import numpy as np


def get_data(n = 1000):
    '''
    TEST data
    X: simulate tweeter sentiment data
    y: simulate stock price
    '''
    nDays = 7
    nTweet = 1000

    sentiment = np.random.uniform(low = -1.0, high = 1.0, size = (n, nDays, nTweet))
    confidence = np.random.uniform(low = 0.0, high = 1.0, size = (n, nDays, nTweet))

    X = np.sum((sentiment * confidence), axis = 2).reshape(n, nDays, 1) # n * nDays * 1
    y = np.sin(X.reshape(n, nDays)) + np.random.normal(loc = 100, scale = 5, size = (n,nDays)) # n x nDays

    # try normalizing label
    ymean = np.tile(np.average(y, axis = 1).reshape(n,1), (1,nDays))
    ystd = np.tile(np.std(y, axis = 1).reshape(n,1).reshape(n,1), (1,nDays))
    y = (y - ymean)/ystd


    return X, y


def get_generator():
    pass


def main(): # test
    X, y = get_data()
    print(X.shape, y.shape)

if __name__ == '__main__':
    main()
