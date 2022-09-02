import numpy as np
import json
from flask import Flask, render_template, request
# import util
import pickle

app = Flask(__name__)
# app = Flask(__name__, template_folder='../client')

model = pickle.load(open('artifacts/house_price_predict_model.pickle', 'rb'))


# __location = None
# __data_columns = None
# __model = None


def get_estimated_price(location, total_sqft, bhk, bath, balcony):
    __model = load_model()
    __data_columns = get_data_columns()

    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bath
    x[1] = balcony
    x[2] = bhk
    x[3] = total_sqft
    if(loc_index >= 0):
        x[loc_index] = 1

    # print("value : ", round(__model.predict([x])[0], 2))
    return round(__model.predict([x])[0], 2)


def get_data_columns():
    with open('artifacts\\columns.json', 'r') as f:
        # print('loading data columns and location.')
        __data_columns = json.load(f)['data_columns']
        # __location = __data_columns[3:]
    return __data_columns


def get_location_names():
    # # print(__location)artifacts\columns.json
    with open('artifacts\columns.json', 'r') as f:
        # print('loading data columns and location.')
        __data_columns = json.load(f)['data_columns']
        __location = __data_columns[3:]
    return __location


def load_model():
    # print('loading saved artifacts')
    # global __data_columns
    # global __location
    # global __model
    __model = None

    # with open('artifacts\\columns.json', 'r') as f:
    #     # print('loading data columns and location.')
    #     __data_columns = json.load(f)['data_columns']
    #     __location = __data_columns[3:]

    with open('artifacts\\house_price_predict_model.pickle', 'rb') as f:
        __model = pickle.load(f)

    return __model


@app.route('/', methods=['GET', 'POST'])
def home():
    response_loc = get_location_names()
    # location = jsonify(response)'
    # # print("Loc", json.dumps(get_location_names()))
    # response = ["abc", "def"]
    return render_template('index.html', response_loc=response_loc)
    # return render_template('student.html')


# @app.route('/get_location_names')
# def get_location_names():
#     response = jsonify({
#         'locations': get_location_names()
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     # print("res : ", get_location_names())
#     return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    # print("home")
    total_sqft = float(request.form['SquareFt'])
    location = request.form['location']
    bhk = int(request.form['uiBHK'])
    bath = int(request.form['uiBath'])
    balcony = int(request.form['uiBalcony'])
    # print(total_sqft, location, bhk, bath, balcony)
    response = get_estimated_price(
        location, total_sqft, bhk, bath, balcony)
    # response = jsonify({
    #     'estimated_price': util.get_estimated_price(total_sqft)
    # })

    # response.headers.add('Access-Control-Allow-Origin', '*')
    # print(response)

    # output = request.form.to_dict()
    # result = output['result']
    response_loc = get_location_names()
    return render_template('index.html', result=response, response_loc=response_loc)


if __name__ == '__main__':
    # print("Starting flask server.")
    # load_saved_artifacts()
    # print(__location)

    # util.load_saved_artifacts()
    app.run()
