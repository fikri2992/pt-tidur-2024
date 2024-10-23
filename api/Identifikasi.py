import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import minmax_scale
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, MaxPooling1D
from tensorflow.keras.optimizers import Adamax
from sklearn.model_selection import train_test_split
import pywt

class Identifikasi:
    def __init__(self, var):
        self.var = var
        self.datauji = None
        self.kelas = None
        self.model_waves = None

    def load_data(self, uploaded_file):
        filepath = os.path.join("uploaded_files", uploaded_file.filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        uploaded_file.save(filepath)
        csv_file = pd.read_csv(filepath)
        newdata = [minmax_scale(csv_file.iloc[row, :], feature_range=(-1, 1)) for row in range(len(csv_file))]
        return newdata

    def load_model(self, model_path):
        model_waves = load_model(model_path)
        self.model_waves = model_waves
        return model_waves
    
    def deteksi(self, model, dataTest):
        if self.var == "sleepapnea":
            dataUji = dataTest.reshape(1, 1, -1)  # Adjust to the shape expected by your model
            y = np.argmax(model.predict(dataUji), axis=-1)
            label = y[0]
            if label == 0:
                return "Obstructive Sleep Apnea (OSA)"
            elif label == 1:
                return "Central Sleep Apnea (CSA)"
            elif label == 2:
                return "Tidak Ada Apnea (No-Apnea)"
            else:
                return "Coba Kembali"