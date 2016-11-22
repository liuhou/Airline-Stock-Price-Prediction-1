import os
import datetime
import click
import numpy as np
import importlib
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from keras.models import load_model


def save_history(log_path, loss, acc=None):
    """Save history into files."""
    # save numbers
    history_file = os.path.join(log_path, 'history.txt')
    with open(history_file, 'w') as fhistory:
        fhistory.write('loss: ' + str(loss) + '\n')
        if acc:
            fhistory.write('acc: ' + str(acc) + '\n')

    # plot
    loss_file = os.path.join(log_path, 'loss.png')
    plt.figure()
    plt.plot(np.arange(len(loss)), loss)
    plt.savefig(loss_file, bbox_inches='tight')

    if acc:
        acc_file = os.path.join(log_path, 'acc.png')
        plt.figure()
        plt.plot(np.arange(len(acc)), acc)
        plt.savefig(acc_file, bbox_inches='tight')


def train():
    log_path = 'log/%s/'%('sim2') #'log/%s/'%(datetime.datetime.today())
    module_model = 'rnn.tw-lstm'
    module_data = 'data.tw-data'

    # get model
    print('getting model %s'%(module_model))
    imported_model = importlib.import_module(module_model)
    model = imported_model.get_model()
    print(model.input_shape, model.output_shape)

    # get data
    print('getting data %s'%(module_data))
    imported_data = importlib.import_module(module_data)
    X, y = imported_data.get_data()
    print(X.shape, y.shape)

    # train
    hist = model.fit(X, y, batch_size = 16, nb_epoch = 32)

    # save
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    try:
        model.save(os.path.join(log_path, 'model.hdf5'))
    except:
        print('Cannot save model.')
    save_history(log_path, hist.history.get('loss'),
                 hist.history.get('acc'))


def test():
    model_path = 'log/%s/model.hdf5'%('sim2')
    module_data = 'data.tw-data'

    # get trained model
    model = load_model(model_path)

    # get testing data
    imported_data = importlib.import_module(module_data)
    X_t, y_t = imported_data.get_data(n = 3)
    predictions = model.predict(X_t)

    #print(X_t)
    print(y_t)
    print(predictions)


@click.command()
@click.option('--trainmodel', is_flag = True, default=False)
def main(trainmodel):
    if trainmodel:
        train()
    test()


if __name__ == '__main__':
    main()

