from CheckRideService import CheckRideService
from xml.etree import ElementTree
import requests
import re


class LosAngelesMetroBusService(CheckRideService):

    def check_ride(self, route, stop, agency):
        response = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?'
                                'command=predictions&a=lametro&routeTag=%s&stopId=%s' % (route, stop))

        minutes = []

        root = ElementTree.fromstring(response.content)

        if root.find('Error'):
            return minutes, None

        try:
            predictions = root.find('predictions')
            directions = predictions.findall('direction')
        except Exception:
            return minutes, None

        for direction in directions:
            for prediction in direction:
                minutes.append(prediction.get('minutes'))

        return sorted(minutes, key=int)[:2], self.__format_stop_names(predictions.get('stopTitle'))

    def __format_stop_names(self, name):
        intersection = name.split('&amp;')
        if len(intersection) < 2:
            intersection = name.split('&')
        if len(intersection) < 2:
            intersection = name.split('/')
        formatted_intersection = []
        for street in intersection:
            street = re.sub(r' St(\s|\\.)?$', '', street)
            street = re.sub(r' Ave(\s|\\.)?$', '', street)
            street = re.sub(r' Dr(\s|\\.)?$', '', street)
            street = re.sub(r' Ct(\s|\\.)?$.', '', street)
            street = re.sub(r' Blvd(\s|\\.)?$.', '', street)
            formatted_intersection.append(street)
        return ' and '.join(formatted_intersection)


if __name__ == '__main__':
    print LosAngelesMetroBusService().check_ride('18', '16613', 'la-metro-bus')
