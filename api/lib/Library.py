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
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale  # Add this import
from pylab import *

class Library:
    def __init__(self, var):
        self.var = var
        self.logs = []

    def log(self, message):
        print(message)
        self.logs.append(message)

    def wavelet(self, DataEEG):
        Frek = []
        for i in range(len(DataEEG)):
            C4 = minmax_scale(DataEEG.iloc[i], feature_range=(-1, 1))
            wp = pywt.WaveletPacket(data=C4, wavelet='db4', mode='per')
            Frek1 = wp['aa'].data
            Frek2 = wp['adaaa'].data
            Frek3 = wp['adaada'].data
            Frek.append([np.concatenate((Frek1, Frek2, Frek3), axis=None)])

        vektor_gelombang = np.concatenate((Frek[0]), axis=None)
        self.log("Wavelet Transform: " + str(vektor_gelombang))
        self.log("Panjang Wavelet Transform: " + str(len(vektor_gelombang)))

        return vektor_gelombang

    def CNN(self, datainput):
        conv1d_weights1 = np.array([0., 1., 0.]).reshape((3, 1, 1))

        # Declare kernel weights
        kernel = tf.constant(conv1d_weights1, dtype=tf.float32)

        # Declare max pooling
        max_pool_1d = tf.keras.layers.MaxPooling1D(pool_size=2, padding='valid')

        # Data preparation
        vek = np.array(datainput).reshape(1, -1, 1)
        data = tf.constant(vek, dtype=tf.float32)

        # First layer (Convolution + Pooling)
        res = conv1d(data, kernel, 1, "VALID")
        self.log("Convolution Output: " + str(res.numpy().flatten()))
        self.log("Convolution Output Length: " + str(len(res.numpy().flatten())))

        # Apply ReLU activation
        res_relu = tf.nn.relu(res)
        self.log("ReLU Output: " + str(res_relu.numpy().flatten()))
        self.log("ReLU Output Length: " + str(len(res_relu.numpy().flatten())))

        # Apply Max Pooling
        res2 = np.array(max_pool_1d(res_relu)).flatten()
        self.log("Max Pooling Output Length: " + str(len(res2)))

        return res2

    def deteksi(self, model, dataTest):
        # Log the original shape and size of dataTest
        self.log("Original dataTest shape: " + str(dataTest.shape))
        self.log("Original dataTest size: " + str(dataTest.size))


        if self.var == "sleepapnea":
            # Log the original shape and size of dataTest
            self.log("Original dataTest shape: " + str(dataTest.shape))
            self.log("Original dataTest size: " + str(dataTest.size))

            # Specify the required input size for your model
            required_size = 444  # Change this if your model expects a different input size

            # Adjust dataTest to match the required size
            if dataTest.size > required_size:
                # Truncate dataTest
                dataTest_adjusted = dataTest[:required_size]
                self.log(f"dataTest truncated to {required_size} elements.")
            elif dataTest.size < required_size:
                # Pad dataTest with zeros
                padding = np.zeros(required_size - dataTest.size)
                dataTest_adjusted = np.concatenate((dataTest, padding))
                self.log(f"dataTest padded to {required_size} elements.")
            else:
                dataTest_adjusted = dataTest
                self.log("dataTest size matches the required size.")

            # Reshape dataTest_adjusted
            dataUji = dataTest_adjusted.reshape(1, 1, required_size)
            self.log("dataUji shape after reshaping: " + str(dataUji.shape))

            # Make the prediction
            result = model.predict(dataUji)
            y = np.argmax(result, axis=-1)
            self.log(f"Prediction Result {str(y)} detail: {result}")
            # self.log("Prediction Result: " + str(y)) + " detail: "  + result

            label = ""

        for idx in y:
            label = idx

        if self.var == "sleepapnea":
            if label == 0:
                return "Obstructive Sleep Apnea (OSA)"
            elif label == 1:
                return "Central Sleep Apnea (CSA)"
            elif label == 2:
                return "Tidak Ada Apnea (No-Apnea)"
            else:
                return "Coba Kembali"


    def predict(self, model, dataTest):
        # Log the original shape and size of dataTest
        self.log("Original dataTest shape: " + str(dataTest.shape))
        self.log("Original dataTest size: " + str(dataTest.size))


        if self.var == "sleepapnea":
            # Log the original shape and size of dataTest
            self.log("Original dataTest shape: " + str(dataTest.shape))
            self.log("Original dataTest size: " + str(dataTest.size))

            # Specify the required input size for your model
            required_size = 444  # Change this if your model expects a different input size

            # Adjust dataTest to match the required size
            if dataTest.size > required_size:
                # Truncate dataTest
                dataTest_adjusted = dataTest[:required_size]
                self.log(f"dataTest truncated to {required_size} elements.")
            elif dataTest.size < required_size:
                # Pad dataTest with zeros
                padding = np.zeros(required_size - dataTest.size)
                dataTest_adjusted = np.concatenate((dataTest, padding))
                self.log(f"dataTest padded to {required_size} elements.")
            else:
                dataTest_adjusted = dataTest
                self.log("dataTest size matches the required size.")

            # Reshape dataTest_adjusted
            dataUji = dataTest_adjusted.reshape(1, 1, required_size)
            self.log("dataUji shape after reshaping: " + str(dataUji.shape))

            # Make the prediction
            result = model.predict(dataUji)
            return result
            
    def translate(self, result):
            y = np.argmax(result, axis=-1)
            self.log(f"Prediction Result {str(y)} detail: {result}")
            # self.log("Prediction Result: " + str(y)) + " detail: "  + result

            label = ""

            for idx in y:
                label = idx

            if self.var == "sleepapnea":
                if label == 0:
                    return "Obstructive Sleep Apnea (OSA)"
                elif label == 1:
                    return "Central Sleep Apnea (CSA)"
                elif label == 2:
                    return "Tidak Ada Apnea (No-Apnea)"
                else:
                    return "Coba Kembali"

