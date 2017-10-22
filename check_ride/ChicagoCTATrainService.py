from CheckRideService import CheckRideService


class ChicagoCTATrainService(CheckRideService):

    def check_ride(self, bus, stop, agency):
        return 'CheckChicagoCTATrainService', '1'
