from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model from the pkl file
with open('rfc.pkl', 'rb') as f:
    rf = pickle.load(f)

# Define the OrdinalEncoder
encoder = OrdinalEncoder()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    # Parse the JSON data from the request
    data = request.get_json()

    # Extract the input data
    age = int(data['age'])
    workclass = data['workclass']
    fnlwgt = float(data['fnlwgt'])
    education = data['education']
    education_num = int(data['education-num'])
    marital_status = data['marital-status']
    occupation = data['occupation']
    relationship = data['relationship']
    race = data['race']
    capital_gain = float(data['capital-gain'])
    capital_loss = float(data['capital-loss'])
    hours_per_week = int(data['hours-per-week'])
    native_country = data['native-country']

    # Create a Pandas DataFrame from the input data
    input_data = pd.DataFrame({
        'age': [age],
        'workclass': [workclass],
        'fnlwgt': [fnlwgt],
        'education': [education],
        'education-num': [education_num],
        'marital-status': [marital_status],
        'occupation': [occupation],
        'relationship': [relationship],
        'race': [race],
        'capital-gain': [capital_gain],
        'capital-loss': [capital_loss],
        'hours-per-week': [hours_per_week],
        'native-country': [native_country]
    })

    # Encode the categorical variables
    input_data_encoded = encoder.fit_transform(input_data)  # Ensure encoder is fitted with the data

    # Make a prediction using the trained model
    prediction = rf.predict(input_data_encoded)

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction[0]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)