import smartcar 
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id ='ae64785d-d7ab-4c00-a039-e4916cc9cec2',
    client_secret = 'df10e885-51d7-4f22-9b1e-4186c501f172',
    redirect_uri = 'https://smartcar-app-229900.appspot.com/exchange',
    scope=['read_vehicle_info', 'read_location'],
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

# used to archive the longitude and latitude in the MySQL database
def logLocation():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    
    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    location = vehicle.location()
    latitude = location["data"]["latitude"]
           longitude = location["data"]["longitude"]
           timestamp = location["age"]
           print(latitude, longitude, timestamp)
           data = csv.writer(f)
           data.writerow([latitude, longitude, timestamp])
           time.sleep(2)
    

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
