import pandas as pd
import numpy as np
import csv
import os
import pywt
import tensorflow as tf
from tensorflow import keras
from keras.utils import to_categorical
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import MaxPooling1D
from keras.optimizers import Adamax
from tensorflow.python.ops.nn_ops import conv1d
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
from pylab import *
import time
from tensorflow.keras.layers import GRU, BatchNormalization
from sklearn.model_selection import KFold

class Pemodelan:
    def __init__(self,var):
        self.inputcnn = []
        self.x_train_waves = None
        self.y_train_waves = None
        self.x_test_waves = None
        self.y_test_waves = None
        self.vektor_out_cnn = None
        self.var = var

    def CNN(self, datainput):
        conv1d_weights1 = np.array([0., 1., 0.]).reshape((3, 1, 1))
        kernel = tf.constant(conv1d_weights1, dtype=tf.float32)
        max_pool_1d = tf.keras.layers.MaxPooling1D(pool_size=2, padding='valid')
        vek = np.array(datainput).reshape(1, -1, 1)
        data = tf.constant(vek, dtype=tf.float32)
        res = conv1d(data, kernel, 1, "VALID")
        res2 = np.array(max_pool_1d(res)).flatten()
        return res2

    def GRU(self, x_train_shape, noclass):
        model = keras.Sequential()
        model.add(GRU(512, activation='relu', input_shape=(x_train_shape), return_sequences=True))
        model.add(BatchNormalization())
        model.add(Dropout(0.1))
        model.add(GRU(256, activation='tanh'))
        model.add(BatchNormalization())
        model.add(Dropout(0.1))
        model.add(Dense(noclass, activation='softmax'))
        optimizer = Adamax(learning_rate=0.0003)
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def split_data(self, vektor_cnn_out):
        X, Y = zip(*vektor_cnn_out)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.8, stratify=Y)
        x_train = np.array(x_train).reshape(len(x_train), 1, -1)
        y_train = np.array(y_train)
        x_test = np.array(x_test).reshape(len(x_test), 1, -1)
        y_test = np.array(y_test)
        noclass = len(np.unique(Y))
        y_train = to_categorical(y_train, noclass)
        y_test = to_categorical(y_test, noclass)
        return x_train, x_test, y_train, y_test, noclass

    def model_waves(self, x_train_shape, noclass):
        return self.GRU(x_train_shape, noclass)

    def training_waves(self, model, x_train, y_train, x_test, y_test):
        start_time = time.time()
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        history = model.fit(x_train, y_train, epochs=50, batch_size=128, validation_data=(x_test, y_test), shuffle=True, verbose=1, callbacks=[early_stopping])
        print("\nTraining model selesai")
        print("Lama waktu learning:", ((time.time() - start_time) / 60))
        score = model.evaluate(x_test, y_test)
        print('Model telah selesai dilakukan pelatihan')
        print('Test Loss:', score[0])
        print('Test Accuracy:', score[1] * 100.0)

    def evaluasi_waves(self, x_train, y_train, x_test, y_test, noclass):
        acc_per_fold = []
        loss_per_fold = []
        time_per_fold = []
        history_all_folds = {}
        inputs = np.concatenate((x_train, x_test), axis=0)
        targets = np.concatenate((y_train, y_test), axis=0)
        kfold = KFold(n_splits=2, shuffle=True)
        start_time = time.time()
        fold_no = 1

        for train, test in kfold.split(inputs, targets):
            fold_start_time = time.time()
            model = self.GRU(x_train.shape[1:], noclass)
            history = model.fit(inputs[train], targets[train], batch_size=128, epochs=50, verbose=1)
            history_all_folds[fold_no] = history.history
            scores = model.evaluate(inputs[test], targets[test], verbose=0)
            acc_per_fold.append(scores[1] * 100)
            loss_per_fold.append(scores[0])
            fold_end_time = time.time()
            fold_duration = (fold_end_time - fold_start_time) / 60
            time_per_fold.append(fold_duration)
            fold_no += 1

        print('Average scores for all folds:')
        print(f'> Accuracy: {np.mean(acc_per_fold)} (+- {np.std(acc_per_fold)})')
        print(f'> Loss: {np.mean(loss_per_fold)}')
        print(f'> Average Time: {np.mean(time_per_fold):.2f} minutes (+- {np.std(time_per_fold):.2f})')
        total_time = (time.time() - start_time) / 60
        print("Total waktu learning:", total_time, "minutes")
        score = model.evaluate(x_test, y_test)
        print('Test Loss:', score[0])
        print('Test Accuracy:', score[1] * 100.0)

    def model_save_waves(self, model, destination=""):
        model.save(destination + "model_" + "C4_M1" + ".h5")
