from CheckRideService import CheckRideService
import requests
import os


class ChicagoCTABusService(CheckRideService):

    def check_ride(self, route, stop, agency):
        response = requests.get('http://www.ctabustracker.com/bustime/api/v2/getpredictions?'
                                'key=%s&rt=%s&stpid=%s&top=2&format=json' %
                                (os.environ['%s_api_key' % agency.replace('-', '_')], route, stop))

        minutes = []

        bustime_response = response.json()['bustime-response']

        if 'error' in bustime_response:
            return minutes, None

        predictions = bustime_response['prd']

        for prdt in predictions:
            minutes.append(prdt['prdctdn'])

        stop_name = predictions[0]['stpnm']
        if stop_name:
            stop_name = stop_name.replace('&', 'and')

        return minutes, stop_name


if __name__ == '__main__':
    os.environ['chicago_cta_bus_api_key'] = 'api_key'
    print ChicagoCTABusService().check_ride('151', '1108', 'chicago-cta-bus')
