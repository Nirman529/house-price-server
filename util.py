import pickle
import json
import numpy as np

__location = None
__data_columns = None
__model = None


def get_estimated_price(location, total_sqft, bhk, bath, balcony):
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

    print("value : ", round(__model.predict([x])[0], 2))
    return round(__model.predict([x])[0], 2)


def get_location_names():
    # print(__location)
    return __location


def load_saved_artifacts():
    print('loading saved artifacts')
    global __data_columns
    global __location
    global __model

    with open('artifacts\\columns.json', 'r') as f:
        print('loading data columns and location.')
        __data_columns = json.load(f)['data_columns']
        __location = __data_columns[3:]

    with open('artifacts\\house_price_predict_model.pickle', 'rb') as f:
        __model = pickle.load(f)

    print('artifacts loaded..')


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
