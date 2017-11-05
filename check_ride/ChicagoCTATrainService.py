from CheckRideService import CheckRideService
import requests
import os
from datetime import datetime
import pytz
import logging as log


class ChicagoCTATrainService(CheckRideService):

    def __init__(self):
        self.mapper = {
            'brown': 'Brn',
            'green': 'G',
            'orange': 'Org',
            'pink': 'Pink',
            'purple': 'P',
            'red': 'Red',
            'yellow': 'Y',
            'blue': 'Blue'
        }

    def check_ride(self, route, stop, agency):
        minutes = []

        try:
            route = self.mapper[route]
        except KeyError:
            log.error('Invalid rt: %s', route)
            return minutes, None

        response = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?'
                                'key=%s&rt=%s&stpid=%s&max=2&outputType=JSON' %
                                (os.environ['%s_api_key' % agency.replace('-', '_')], route, stop))

        response = response.json()['ctatt']

        if response['errCd'] != '0' or 'eta' not in response:
            log.error(response)
            return minutes, None

        predictions = response['eta']

        for prdt in predictions:
            arrival = pytz.timezone('America/Chicago').localize(
                datetime.strptime(prdt['arrT'], '%Y-%m-%dT%H:%M:%S'), is_dst=None).astimezone(pytz.utc) - \
                      pytz.utc.localize(datetime.utcnow(), is_dst=None)
            minutes.append(int(arrival.total_seconds() / 60))

        stop_name = predictions[0]['staNm']
        stop_name.replace('-', ' and ', 1)
        stop_name.replace('/', ' and ', 1)

        return minutes, stop_name

if __name__ == '__main__':
    os.environ['chicago_cta_train_api_key'] = 'api_key'
    print ChicagoCTATrainService().check_ride('red', '30267', 'chicago-cta-train')
