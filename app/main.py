import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id ='ae64785d-d7ab-4c00-a039-e4916cc9cec2',
    client_secret = 'df10e885-51d7-4f22-9b1e-4186c501f172',
    redirect_uri = 'http://localhost:8000/exchange',
    scope=['read_vehicle_info'],
    test_mode=True
    )


@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return '', 200

@app.route('/location', methods=['GET'])
def location():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    
    # instantiate the first vehicle in the vehicle id list
    car1 = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    loc = car1.location()

    return jsonify(loc)

@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()

    print(info)

    return jsonify(info)

if __name__ == '__main__':
    app.run(port=8000)
