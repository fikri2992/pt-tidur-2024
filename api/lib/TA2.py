from flask import Flask, render_template, send_file, make_response, url_for, Response, request, redirect
import pickle
import sys
sys.path.append(".")
import Library
from Library import Library
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import csv
from tensorflow import keras
from keras.models import load_model
from keras.layers import GRU, GRUCell
from keras.initializers import glorot_uniform, Orthogonal  # Import Orthogonal initializer
from tensorflow.python.ops.nn_ops import conv1d
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
import io
from csv import writer


app = Flask(__name__)

# Custom GRU class to handle unrecognized arguments
class CustomGRU(GRU):
    def __init__(self, *args, **kwargs):
        # Remove unrecognized arguments
        kwargs.pop('time_major', None)
        kwargs.pop('implementation', None)
        super().__init__(*args, **kwargs)

# Load your model with Orthogonal initializer and Custom GRU
model = load_model('model_C4_M1.h5', custom_objects={'Orthogonal': Orthogonal, 'GRU': CustomGRU})

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/Hasil', methods=['POST'])
def Hasil():
    if request.method == 'POST':
        newdata = []
        if request.files:
            uploaded_file = request.files['data-uji']
            filepath = os.path.join(uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath) as file:
                csv_file = pd.read_csv(file)
                for row in range(len(csv_file)):
                    data = minmax_scale(csv_file.iloc[row, :], feature_range=(-1, 1))
                    newdata.append(data)

        dataTest = pd.DataFrame(newdata)
        print(dataTest.shape)
        ukuran = dataTest.size
        print(ukuran, file=sys.stderr)

        vareeg = "sleepapnea"
        lib = Library(vareeg)
        wav = lib.Wavelet_filter(dataTest)
        cnn = lib.ekstraksi(wav)
        kelas = lib.getKelas(model, cnn)

        return render_template('identifikasi.html', hasil=kelas, name=uploaded_file.filename)
    else:
        return render_template('identifikasi.html', hasil="-")

@app.route('/petunjuk')
def petunjuk():
    return render_template("petunjuk.html")

@app.route('/identifikasi')
def identifikasi():
    return render_template("identifikasi.html", hasil="-", last_updated=dir_last_updated('static'))

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)