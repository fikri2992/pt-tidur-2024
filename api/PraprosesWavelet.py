import pandas as pd
import numpy as np
import os
import pywt
import tensorflow as tf
from tensorflow import keras
from keras.utils import to_categorical
from keras.layers import Dense, Dropout, Activation, Flatten, MaxPooling1D, BatchNormalization, GRU
from keras.optimizers import Adamax
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import minmax_scale
from imblearn.over_sampling import SMOTE
from collections import Counter

class PraprosesWavelet:
    def __init__(self,var):
        self.datalatih = []
        self.vektor_input = []
        self.var = var

    def data_latih(self, data_path, classes):
        newdata = []
        for kelas in classes:
            pathkelas = os.path.join(data_path, kelas)
            numkelas = classes.index(kelas)
            for edf in os.listdir(pathkelas):
                edf_array = pd.read_csv(os.path.join(pathkelas, edf))
                for j in range(len(edf_array)):
                    row_data = edf_array.iloc[j, 0]
                    try:
                        float_data = np.array([float(x) for x in row_data.split(';')])
                        scaled_data = minmax_scale(float_data, feature_range=(-1, 1))
                        newdata.append([scaled_data, numkelas])
                    except ValueError as e:
                        print(f"Non-numeric data found in file: {edf}, row: {j}, error: {e}")
        x, y = zip(*newdata)
        counter = Counter(y)
        print("Number of Each class:", counter)
        oversample = SMOTE()
        x_smote, y_smote = oversample.fit_resample(np.array(x), np.array(y))
        counter = Counter(y_smote)
        print("Number of Each class after SMOTE:", counter)
        return list(zip(x_smote, y_smote))

    def wavelet(self, DataEEG):
        vektor_gelombang = []
        for i in range(len(DataEEG)):
            C4 = minmax_scale(DataEEG.iloc[i], feature_range=(-1, 1))
            Frek = []

            wp = pywt.WaveletPacket(data=C4, wavelet='db4', mode='per')
            Frek1 = wp['aa'].data
            Frek2 = wp['adaaa'].data
            Frek3 = wp['adaada'].data

            Frek.append(np.concatenate((Frek1, Frek2, Frek3), axis=None))

            vektor_gelombang.append(np.concatenate((Frek[0]), axis=None))

        return vektor_gelombang
