# x - input. (N_samples x N_features) meta data + embedded tweets + embedded usernames
# y - labels. 1 fake, 0 real

import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras import optimizers
from time import gmtime, strftime
import os
import matplotlib.pyplot as plt
import pickle
import random
import tensorflow as tf


def train(x, y):
    n_epochs = 20
    n_batch = 5

    # mix data
    idx = np.random.permutation(x.shape[0])
    x = x[idx]
    y = y[idx]

    g = tf.Graph()
    with g.as_default():
        model = Sequential()
        model.add(Dense(32, activation='relu', input_dim=x.shape[1]))
        model.add(Dense(1, activation='sigmoid'))
        sgd = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=sgd,
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        dir_name = strftime("%Y-%m-%d %H-%M-%S", gmtime())  # make a directory for saving the model
        os.mkdir(dir_name)
        checkpointer = keras.callbacks.ModelCheckpoint(filepath='./' + dir_name + '/weights.{epoch:02d}-{val_acc:.2f}.hdf5', verbose=1)
        # Train the model
        train_hist = model.fit(x, y, epochs=n_epochs, batch_size=n_batch, validation_split=0.1, verbose=2, callbacks=[checkpointer])
    # train_loss = train_hist.history['loss']
    # val_loss = train_hist.history['val_loss']
    train_loss = train_hist.history['acc']
    val_loss = train_hist.history['val_acc']
    plt.plot(np.arange(n_epochs), train_loss, label='train')
    plt.plot(np.arange(n_epochs), val_loss, label='val')
    plt.legend()
    plt.show()


def evaluate(x, save_path='../source/2018-09-16 03-22-43/weights.16-0.68.hdf5'):
    # normalize with train statistics
    with open('../data/norm_train_params.pkl', 'rb') as f:
        train_mean, train_std = pickle.load(f)
    x = (x - train_mean) / train_std
    loaded_model = load_model(save_path)
    est = loaded_model.predict(x.reshape(-1,49))
    return est.flatten()


if __name__ == "__main__":
    with open('../data/processed_data.pkl', 'rb') as f:
        data, lbls = pickle.load(f)
    # est = evaluate(data[10:20], '../source/2018-09-16 03-14-26/weights.05-0.57.hdf5')
    # est2 = evaluate(data[:10], '../source/2018-09-16 03-14-26/weights.05-0.57.hdf5')
    # equal fake / real samples
    n_min = np.minimum(np.sum(lbls == 0), np.sum(lbls == 1))
    idx = np.concatenate([random.sample(list(np.where(lbls == 0)[0]), n_min), random.sample(list(np.where(lbls == 1)[0]), n_min)])
    # normalize the data
    train_mean = np.mean(data[idx], axis=0)
    train_std = np.std(data[idx], axis=0)
    train_data = (data[idx] - train_mean) / train_std
    # save normalization params
    # with open('../data/norm_train_params.pkl', 'wb') as f:
    #     pickle.dump([train_mean, train_std],f)
    # train(train_data, lbls[idx])




