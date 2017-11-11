import logging as log
import os
from flask import Flask, request, Response, jsonify
from check_ride.CheckRideServiceFactory import CheckRideServiceFactory
from get_ride.GetRideService import get_ride
from set_ride.SetRideService import set_ride
from helper.ResponseConstants import ResponseConstants

app = Flask(__name__)


@app.route('/check', methods=['GET'])
def check():
    route = request.args.get('route')
    stop = request.args.get('stop')
    agency = request.args.get('agency')
    
    log.info('route=%s, stop=%s, agency=%s' % (route, stop, agency))

    if not route or not stop or not agency:
        return __respond(ResponseConstants.CHK_MISSING_PARAM, [route, stop, agency])

    service = CheckRideServiceFactory.get_service(agency)
    if not service:
        return __respond(ResponseConstants.CHK_MISSING_SERVICE)

    minutes, stop_name = service.check_ride(route, stop, agency)

    response = ResponseConstants.SUCCESS_RESP
    response['message'] = {'minutes': minutes, 'stop_name': stop_name or ''}
    return __respond(response)


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
                                             
    log.info('user=%s, route=%s, stop=%s, preset=%s, agency=%s' % (user, route, stop, preset, agency))

    if not user:
        return __respond(ResponseConstants.ALL_MISSING_USER)

    if not route or not stop or not preset or not agency:
        return __respond(ResponseConstants.SET_MISSING_PARAM, [route, stop, preset, agency])

    if set_ride(user, route, stop, preset, agency) != 200:
        return __respond(ResponseConstants.SET_FAILURE, [route, stop, preset, agency])

    response = ResponseConstants.SUCCESS_RESP
    response['message'] = 'success'
    return __respond(response)


@app.route('/get', methods=['GET'])
def get():
    user = request.args.get('user')
    preset = request.args.get('preset') or 'A'
    agency = request.args.get('agency')
                                             
    log.info('user=%s, preset=%s, agency=%s' % (user, preset, agency))

    if not user:
        return __respond(ResponseConstants.ALL_MISSING_USER)

    if not agency:
        return __respond(ResponseConstants.GET_MISSING_AGENCY)

    route, stop = get_ride(user, preset, agency)

    if not route or not stop:
        return __respond(ResponseConstants.GET_MISSING_ROUTE_STOP, [preset])

    service = CheckRideServiceFactory.get_service(agency)
    minutes, stop_name = service.check_ride(route, stop, agency)

    response = ResponseConstants.SUCCESS_RESP
    response['message'] = {'minutes': minutes, 'stop_name': stop_name or '', 'route': route, 'stop': stop}
    return __respond(response)


def __respond(error_constant, params=None):
    if params:
        params = map((lambda x: 'None' if not x else x), params)
    else:
        params = []

    if isinstance(error_constant['message'], dict):
        message = error_constant['message']
    else:
        message = '%s%s%s' % (error_constant['message'], ': ' if len(params) else '', ', '.join(params))
    json = jsonify(error_code=error_constant['error'], message=message).get_data(as_text=True)
    if error_constant['status'] in [400, 500]:
        log.warn(json)
    return Response(json, status=error_constant['status'], mimetype='application/json')


if __name__ == '__main__':
    os.environ['user_table'] = 'EZTransit_Users'
    os.environ['audit_table'] = 'EZTransit_Audit'
    os.environ['chicago_cta_train_api_key'] = 'api_key'
    os.environ['chicago_cta_bus_api_key'] = 'api_key'
    app.run()
