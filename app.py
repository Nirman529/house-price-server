from unittest import result
from flask import Flask, render_template, jsonify, request, make_response, url_for, redirect
import numpy as np
import util
import pickle
import requests
import json

app = Flask(__name__)
# app = Flask(__name__, template_folder='../client')

model = pickle.load(open('artifacts/house_price_predict_model.pickle', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    balcony = int(request.form['balcony'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath, balcony)
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    print(response)

    output = request.form.to_dict()
    result = output['result']

    return render_template('index.html', result=result)


if __name__ == '__main__':
    print("Starting flask server.")
    util.load_saved_artifacts()
    app.run()
