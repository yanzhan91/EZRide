from CheckRideService import CheckRideService
import requests
import re
import os
import logging as log


class DCMetroBusService(CheckRideService):

    def check_ride(self, route, stop, agency):
        response = requests.get('https://api.wmata.com/NextBusService.svc/json/jPredictions?StopID=%s' % stop,
                                headers={'api_key': os.environ['%s_api_key' % agency.replace('-', '_')]})

        minutes = []

        bustime_response = response.json()

        if 'Predictions' not in bustime_response:
            log.error('agency=%s, route=%s, stop=%s, msg=%s', agency, route, stop, bustime_response)
            return minutes, None

        predictions = bustime_response['Predictions']

        for prdt in predictions:
            if prdt['RouteID'] == route:
                minutes.append(prdt['Minutes'])

        stop_name = bustime_response['StopName']
        if stop_name:
            stop_name = self.__format_stop_names(stop_name)

        return minutes, stop_name

    def __format_stop_names(self, name):
        name = re.sub(r'\+', 'and', name)
        name = re.sub(r'\s?St(\s?|$)', ' ', name)
        name = re.sub(r'\s?Ave(\s?|$)', ' ', name)
        name = re.sub(r'\s?Dr(\s?|$)', ' ', name)
        name = re.sub(r'\s?Ct(\s?|$)', ' ', name)
        name = re.sub(r'\s?Blvd(\s?|$)', ' ', name)
        return name


if __name__ == '__main__':
    print DCMetroBusService().check_ride('70', '1001195', 'dc-metro-bus')
