class ResponseConstants:
    SUCCESS_RESP = {
        'error': 0,
        'status': 200,
        'message': ''
    }
    CHK_MISSING_PARAM = {
        'error': 10101,
        'status': 400,
        'message': 'Missing route, stop, or agency'
    }
    CHK_MISSING_SERVICE = {
        'error': 10102,
        'status': 500,
        'message': 'Internal server error: Failed to get agency check_ride service'
    }
    SET_MISSING_PARAM = {
        'error': 10201,
        'status': 400,
        'message': 'Missing route, stop, preset or agency'
    }
    SET_FAILURE = {
        'error': 10202,
        'status': 500,
        'message': 'Internal server error: Failed to set ride'
    }
    GET_MISSING_AGENCY = {
        'error': 10301,
        'status': 400,
        'message': 'Missing agency'
    }
    GET_MISSING_ROUTE_STOP = {
        'error': 10302,
        'status': 400,
        'message': 'Preset not set'
    }
    ALL_MISSING_USER = {
        'error': 10401,
        'status': 400,
        'message': 'Missing user'
    }
