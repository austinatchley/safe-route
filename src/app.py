from argparse import ArgumentParser
from flask import Flask, request, jsonify
import requests
from datetime import timedelta, date

app = Flask(__name__)
time_init_offset = timedelta(days = 365)
local_dist = "0.1mi"
neighborhood_dist = "10mi"
local_neighborhood_ratio = (0.1 ** 2) / (10 ** 2)


# Custom Exception used for returning meaningful messages to API requests
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv

# Handler for InvalidUsage exceptions
@app.errorhandler(InvalidUsage)
def handleError(e):
    # Parse error and send it to the user in a response
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


def main():
    parser = ArgumentParser(description="Safe Route Server")
    parser.add_argument("--debug", "-D", action="store_true", help="enable Flask debug mode")
    parser.add_argument("--port", "-p", default=5000, nargs="?", help="port for Flask server")
    args = parser.parse_args()

    app.run(debug=args.debug, port=args.port)


def get_time_init_end():
    # time_end = "2020-04-29T00:00:00.000Z"
    time_end = date.today()
    time_init = time_end - time_init_offset

    time_init_str = time_init.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    time_end_str = time_init.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return time_init_str, time_end_str


def get_url(latitude, longitude, distance):
    time_init, time_end = get_time_init_end()

    return ("https://api.crimeometer.com/v1/incidents/stats?"
        "lat=" + latitude + ""
        "&lon=" + longitude + ""
        "&datetime_ini=" + time_init + ""
        "&datetime_end=" + time_end + ""
        "&distance=" + distance)


# Calculates the safety value for a single location
def calculate_safety(latitude, longitude):
    headers = {"Content-Type": "application/json", "x-api-key": "B6XW4GXWZA9ruQheGLFGg2K9e7iWCz4Z6rwsfcz7"}

    print "URL: " + get_url(latitude, longitude, local_dist)

    try:
        local_response = requests.get(url = get_url(latitude, longitude, local_dist), headers = headers)
        neighborhood_response = requests.get(url = get_url(latitude, longitude, neighborhood_dist), headers = headers)

        print local_response.json()
        print neighborhood_response.json()

        local_incidents = local_response.json()['total_incidents']
        neighborhood_incidents = neighborhood_response.json()['total_incidents']
    except Exception as e:
        raise InvalidUsage("Unknnown error: " + str(e))

    if neighborhood_incidents == 0:
        crime_proportion = 0.0
    else:
        crime_proportion = max(0.0, local_incidents / neighborhood_incidents)

    if crime_proportion == 0.0:
        return 1

    return local_neighborhood_ratio / crime_proportion


def parse_location(location):
    parsed_loc = location.split(',')

    if len(parsed_loc) < 2:
        raise InvalidUsage("A location needs comma-separated longitude and latitude")

    return parsed_loc[0], parsed_loc[1]


########################################
# API definition
@app.route('/', methods=['GET'])
def home():
    return {"page": "home"}


# Receives POST request containing a location
# Returns the safety value at this location
@app.route('/safety/loc', methods=['POST'])
def safety_at_point():
    if request is None or not request.is_json:
        raise InvalidUsage('Request is in an invalid state', status_code=400)

    try:
        location = request.json["location"]
    except:
        raise InvalidUsage('Location required', status_code=400)

    longitude, latitude = parse_location(location)
    safety = calculate_safety(longitude, latitude)

    return {"page": "safety_at_loc", "safety": safety}


# Receives POST request containing a series of locations, representing a route
# Returns the safety value on this route
@app.route('/safety/route', methods=['POST'])
def safety_on_route():
    if request is None or not request.is_json:
        raise InvalidUsage('Request is in an invalid state', status_code=400)

    try:
        locations = request.json["locations"]
    except:
        raise InvalidUsage('Locations required', status_code=400)

    safety = 0.0
    for location in locations:
        longitude, latitude = parse_location(location)
        safety += calculate_safety(longitude, latitude)

    return {"page": "safety_on_route", "safety": safety}


if __name__ == "__main__":
    main()