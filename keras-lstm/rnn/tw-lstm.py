from keras.models import Sequential
from keras.layers import LSTM, Dense, Reshape

def get_model():
    model = Sequential()

    model.add(LSTM(7, input_shape = (7, 1), activation = 'sigmoid'))
    model.add(Reshape((7,1)))
    model.add(LSTM(7, activation = 'linear'))
    #model.add(Dense(1, activation = 'linear')) # simplest regression
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model

