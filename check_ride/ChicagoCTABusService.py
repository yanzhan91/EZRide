from CheckRideService import CheckRideService
import requests
import os


class ChicagoCTABusService(CheckRideService):

    def check_ride(self, route, stop, agency):
        response = requests.get('http://www.ctabustracker.com/bustime/api/v2/getpredictions?'
                                'key=%s&rt=%s&stpid=%s&top=2&format=json' %
                                (os.environ['%s-api_key' % agency], route, stop))

        minutes = []

        bustime_response = response.json()['bustime-response']

        if 'error' in bustime_response:
            return minutes, None

        predictions = bustime_response['prd']

        for prdt in predictions:
            minutes.append(prdt['prdctdn'])

        return minutes, predictions[0]['stpnm']


if __name__ == '__main__':
    os.environ['chicago-cta-bus-api_key'] = 'api_key'
    print ChicagoCTABusService().check_ride('151', '1108', 'chicago-cta-bus')
