from flask import Flask, render_template, request, redirect, jsonify, url_for
from joblib import dump, load
import pandas as pd 
import numpy as np

app = Flask(__name__)

save_path = "saved_model/"
model_name = "model"

#patient1 = [ 32, 120, 90, 7.5, 98]

#patient1 = np.array([patient1])

#GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), str(save_path + model_name + ".joblib"))


@app.route('/predict', methods=['POST', 'GET'])
def prod():

    print(request.json['age'])

    patientSympts = [request.json['age'], request.json['SystolicBP'], request.json['DiastolicBP'], request.json['bs'], request.json['bodytemp']]
    patient1 = np.array([patientSympts])

    try:
        # Load Trained Model
        clf = load(str(save_path + model_name + ".joblib"))
        result = clf.predict(patient1)
        print(result)

        return str(result)

        
    except Exception as e:
        print(e)
        return e

if __name__ == "__main__":
    app.run(debug=True)