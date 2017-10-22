import logging
import os
from flask import Flask, request, Response, jsonify
from check_ride.CheckRideServiceFactory import CheckRideServiceFactory
from get_ride.GetRideService import get_ride
from set_ride.SetRideService import set_ride

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/check', methods=['GET'])
def check():
    route = request.args.get('route')
    stop = request.args.get('stop')
    agency = request.args.get('agency')

    if not route or not stop or not agency:
        return __respond('Invalid route, stop, or agency: %s, %s, %s' % (route, stop, agency), status=400)

    service = CheckRideServiceFactory.get_service(agency)
    if not service:
        return __respond('Internal server error: Failed to get agency check_ride service: %s' % agency, status=500)

    minutes, stop_name = service.check_ride(route, stop, agency)

    return __respond({'minutes': minutes, 'stop_name': stop_name}, status=200)


@app.route('/add', methods=['POST'])
def add():
    try:
        user = request.form['user']
    except KeyError:
        user = None

    try:
        route = request.form['route']
    except KeyError:
        route = None

    try:
        stop = request.form['stop']
    except KeyError:
        stop = None

    try:
        preset = request.form['preset']
    except KeyError:
        preset = None

    try:
        agency = request.form['agency']
    except KeyError:
        agency = None

    if not user:
        return __respond('User missing or invalid', status=400)

    if not route or not stop or not agency:
        return __respond(
            'Invalid route, stop, preset or agency: %s, %s, %s, %s' % (route, stop, preset, agency), status=400)

    if set_ride(user, route, stop, preset, agency):
        __respond('Internal server error: Failed to set ride', status=500)

    return 'Adding'


@app.route('/get', methods=['GET'])
def get():
    user = request.args.get('user')
    preset = request.args.get('preset') or '1'
    agency = request.args.get('agency')

    if not user:
        return __respond('User missing or invalid', status=400)

    if not agency:
        return __respond('Invalid agency: %s' % agency, status=400)

    route, stop = get_ride(user, preset, agency)

    if not route or not stop:
        return __respond('Preset not set: %s' % preset, status=400)

    service = CheckRideServiceFactory.get_service(agency)
    minutes, stop_name = service.check_ride(route, stop, agency)

    return __respond({'minutes': minutes, 'stop_name': stop_name}, status=200)


def __respond(message, status):
    json = jsonify(status=status, message=message).get_data(as_text=True)
    if status in [400, 500]:
        logging.warn(json)
    return Response(str(json), status=status, mimetype='application/json')


if __name__ == '__main__':
    os.environ['user_table'] = 'EZTransit_Users'
    os.environ['audit_table'] = 'EZTransit_Audit'
    os.environ['chicago-cta-train-api_key'] = 'api_key'
    os.environ['chicago-cta-bus-api_key'] = 'api_key'
    app.run()
