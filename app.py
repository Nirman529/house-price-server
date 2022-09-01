from flask import Flask, render_template, jsonify, request, make_response, url_for, redirect
import numpy as np
import util
import pickle

app = Flask(__name__)
# app = Flask(__name__, template_folder='../client')

model = pickle.load(open('artifacts/house_price_predict_model.pickle', 'rb'))


@app.route('/')
def home():
    response_loc = util.get_location_names()
    # location = jsonify(response)'
    # print("Loc", json.dumps(get_location_names()))
    # response = ["abc", "def"]
    return render_template('index.html', response_loc=response_loc)
    # return render_template('student.html')


@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    print("res : ", util.get_location_names())
    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    print("home")
    total_sqft = float(request.form['SquareFt'])
    location = request.form['location']
    bhk = int(request.form['uiBHK'])
    bath = int(request.form['uiBath'])
    balcony = int(request.form['uiBalcony'])
    print(total_sqft, location, bhk, bath, balcony)
    response = util.get_estimated_price(
        location, total_sqft, bhk, bath, balcony)
    # response = jsonify({
    #     'estimated_price': util.get_estimated_price(total_sqft)
    # })

    # response.headers.add('Access-Control-Allow-Origin', '*')
    print(response)

    # output = request.form.to_dict()
    # result = output['result']
    response_loc = util.get_location_names()
    return render_template('index.html', result=response, response_loc=response_loc)


if __name__ == '__main__':
    print("Starting flask server.")
    util.load_saved_artifacts()
    app.run()
