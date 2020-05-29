from argparse import ArgumentParser
from flask import Flask, request, jsonify

app = Flask(__name__)

def main():
    parser = ArgumentParser(description="Safe Route Server")
    parser.add_argument("--debug", "-D", action="store_true", help="enable Flask debug mode")
    parser.add_argument("--port", "-p", default=5000, nargs="?", help="port for Flask server")
    args = parser.parse_args()

    app.run(debug=args.debug, port=args.port)

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

@app.route('/', methods=['GET'])
def home():
    return {"page": "home"}

# Receives POST request containing a location
# Returns the safety value at this location
@app.route('/safety/point', methods=['POST'])
def safety_at_point():
    if request is None or not request.is_json:
        raise InvalidUsage('Request is in an invalid state', status_code=400)

    return {"page": "safety_at_point"}

# Receives POST request containing a series of locations, representing a route
# Returns the safety value on this route
@app.route('/safety/route', methods=['POST'])
def safety_on_route():
    if request is None or not request.is_json:
        raise InvalidUsage('Request is in an invalid state', status_code=400)

    return {"page": "safety_on_route"}

if __name__ == "__main__":
    main()