from keras.models import Sequential
from keras.layers import LSTM, Dense, Reshape

def get_model():
    model = Sequential()

    model.add(LSTM(32, input_shape = (7, 1), activation = 'relu'))
    model.add(Reshape((32,1)))
    model.add(LSTM(7, activation = 'linear'))
    #model.add(Dense(1, activation = 'linear')) # simplest regression
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model

