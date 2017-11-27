from check_ride.CheckRideService import CheckRideService
import requests
import os
import pytz
from datetime import datetime


class PortlandTriMetBus(CheckRideService):
    def check_ride(self, route, stop, agency):
        response = requests.get('https://developer.trimet.org/ws/V1/arrivals?'
                                'json=true&appID=%s&locIDs=%s' %
                                (os.environ['%s_api_key' % agency.replace('-', '_')], stop))

        minutes = []

        result_set = response.json()['resultSet']

        if 'errorMessage' in result_set or 'arrival' not in result_set:
            return minutes, None

        arrivals = result_set['arrival']

        for arrival in arrivals:
            time = pytz.timezone('US/Pacific').localize(
                datetime.strptime(arrival['estimated'][:-5], '%Y-%m-%dT%H:%M:%S.%f'), is_dst=None).astimezone(pytz.utc) - \
                      pytz.utc.localize(datetime.utcnow(), is_dst=None)
            minutes.append(int(time.total_seconds() / 60))

        stop_name = result_set['location'][0]['desc']
        if stop_name:
            stop_name = stop_name.replace('&', 'and')

        return minutes, stop_name


if __name__ == '__main__':
    os.environ['portland_tri_met_bus_api_key'] = 'portland_tri_met_bus_api_key'
    print PortlandTriMetBus().check_ride('9', '999', 'portland-tri-met-bus')