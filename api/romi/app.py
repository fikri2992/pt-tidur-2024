from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import minmax_scale
import sys
import os
from keras.models import load_model
from keras.layers import GRU
from keras.initializers import Orthogonal
from lib.Library import Library  # Adjusted import

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
def hasil():
    if request.method == 'POST':
        newdata = []
        if request.files:
            uploaded_file = request.files['data-uji']
            filepath = os.path.join(uploaded_file.filename)
            uploaded_file.save(filepath)
            csv_file = pd.read_csv(filepath)
            for row in range(len(csv_file)):
                data = minmax_scale(csv_file.iloc[row, :], feature_range=(-1, 1))
                newdata.append(data)
        
        data_test = pd.DataFrame(newdata)
        vareeg = "sleepapnea"
        lib1 = Library(vareeg)
        wav = lib1.wavelet(data_test)
        cnn = lib1.CNN(wav)
        kelas = lib1.deteksi(model, cnn)

        logs = "\n".join(lib1.logs)
        response = {
            'prediction': kelas,
            'filename': uploaded_file.filename,
            'logs': logs
        }
        return jsonify(response)
        # return render_template('identifikasi.html', hasil=kelas, name=uploaded_file.filename, logs=logs)
    else:
        return render_template('identifikasi.html', hasil="-", logs="")

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
