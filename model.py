# x - input. (N_samples x N_features) meta data + embedded tweets + embedded usernames
# y - labels. 1 real, 0 fake

import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras import optimizers
from time import gmtime, strftime
import os
import matplotlib.pyplot as plt
import pickle


def train(x, y):
    n_epochs = 10
    n_batch = 32

    # mix data
    idx = np.random.permutation(x.shape[0])
    x = x[idx]
    y = y[idx]

    model = Sequential()
    model.add(Dense(32, activation='relu', input_dim=x.shape[1]))
    model.add(Dense(1, activation='sigmoid'))
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    dir_name = strftime("%Y-%m-%d %H:%M:%S", gmtime())  # make a directory for saving the model
    os.mkdir(dir_name)
    checkpointer = keras.callbacks.ModelCheckpoint(filepath='./' + dir_name + '/weights.{epoch:02d}-{val_loss:.2f}.hdf5', verbose=1)
    # Train the model
    train_hist = model.fit(x, y, epochs=n_epochs, batch_size=n_batch, validation_split=0.1, verbose=2, callbacks=[checkpointer])
    train_loss = train_hist.history['loss']
    val_loss = train_hist.history['val_loss']
    plt.plot(np.arange(n_epochs), train_loss, label='train')
    plt.plot(np.arange(n_epochs), val_loss, label='val')
    plt.show()


def evaluate(x, save_path):
    loaded_model = load_model(save_path)
    est = loaded_model.predict(x)
    return est.astype(bool)


if __name__ == "__main__":
    with open('ADAFake/data/numeric_data.pkl', 'rb') as f:
        data, lbls = pickle.load(f)
    train(data, lbls)
    # est = evaluate(x,'')