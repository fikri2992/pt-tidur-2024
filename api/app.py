from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import minmax_scale
import sys
import os
from keras.models import load_model
from keras.layers import GRU
from keras.initializers import Orthogonal
from lib.Library import Library  # Adjusted import
import numpy as np
app = Flask(__name__)

# Custom GRU class to handle unrecognized arguments
class CustomGRU(GRU):
    def __init__(self, *args, **kwargs):
        # Remove unrecognized arguments
        kwargs.pop('time_major', None)
        kwargs.pop('implementation', None)
        super().__init__(*args, **kwargs)

# Load your model with Orthogonal initializer and Custom GRU
model = load_model('C:\\xampp\\htdocs\\PTTidur2024\\api\\model_C4_M1.h5', custom_objects={'Orthogonal': Orthogonal, 'GRU': CustomGRU})
#add api to check length of file uploaded 
@app.route('/check_file_length', methods=['POST'])
def check_file_length():
    if request.method == 'POST':
        uploaded_file = request.files['data-uji']
        filepath = os.path.join(uploaded_file.filename)
        uploaded_file.save(filepath)
        csv_file = pd.read_csv(filepath)
        length = csv_file
        return jsonify({'length': length})
    else:
        #send api error response here
        return jsonify({'error': 'Invalid request method'}), 400 # Bad Request
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/Hasil', methods=['POST'])
def hasil():
    if request.method == 'POST':
        newdata = []
        print(request.files)
        if request.files:
            uploaded_file = request.files['data-uji']
            print(uploaded_file.filename)
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
        print(len(wav))
        # print len of wav length        
        cnn = lib1.CNN(wav)
        predictions = lib1.predict(model, cnn) # Get prediction probabilities
        kelas = lib1.translate(predictions)

        logs = "\n".join(lib1.logs)
        confidence = np.max(predictions) * 100
        response = {
            'prediction': kelas,
            'confidence': f"{confidence:.2f}%",  # Add confidence to response
            'filename': uploaded_file.filename,
            'logs': logs
        }
        return jsonify(response)
        # return render_template('identifikasi.html', hasil=kelas, name=uploaded_file.filename, logs=logs)
    else:
        #send api error response here
        return jsonify({'error': 'Invalid request method'}), 400 # Bad Request

@app.route('/predict', methods=['POST'])
def infer():
    if request.method == 'POST':
        newdata = []
        # Get the JSON object from the request body
        data_json = request.get_json()
        if data_json:
            # Extract the "data" key
            values_list = data_json.get('data')
            if values_list and isinstance(values_list, list):
                # Process each array in the list
                for values in values_list:
                    if isinstance(values, list):
                        # Ensure all values are numeric
                        try:
                            values = [float(value) for value in values]
                        except ValueError:
                            return jsonify({'error': 'All elements in data arrays must be numbers.'}), 400
                        # Scale the data using minmax_scale
                        data = minmax_scale(values, feature_range=(-1, 1))
                        newdata.append(data)
                    else:
                        return jsonify({'error': 'Each item in "data" must be a list.'}), 400
            else:
                # Handle the case where "data" key is missing or not a list
                return jsonify({'error': 'Invalid data format. Expected JSON with "data" key containing a list of lists.'}), 400
        else:
            # Handle the case where data_json is None or empty
            return jsonify({'error': 'No data provided'}), 400

        # Convert 'newdata' to a DataFrame
        data_test = pd.DataFrame(newdata)
        vareeg = "sleepapnea"
        lib1 = Library(vareeg)

        # Process the data using your existing workflow
        wav = lib1.wavelet(data_test)
        print(len(wav))
        cnn = lib1.CNN(wav)
        predictions = lib1.predict(model, cnn)  # Get prediction probabilities
        kelas = lib1.translate(predictions)

        logs = "\n".join(lib1.logs)
        confidence = np.max(predictions) * 100
        response = {
            'prediction': kelas,
            'confidence': f"{confidence:.2f}%",  # Add confidence to response
            'logs': logs
        }
        return jsonify(response)
    else:
        # Send API error response for invalid request method
        return jsonify({'error': 'Invalid request method'}), 400  # Bad Request    
    

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

