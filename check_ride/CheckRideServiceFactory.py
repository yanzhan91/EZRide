from ChicagoCTABusService import ChicagoCTABusService
from ChicagoCTATrainService import ChicagoCTATrainService
from AustinMetroBusService import AustinMetroBusService
from SanFranciscoMuniBusService import SanFranciscoMuniBusService


class CheckRideServiceFactory(object):

    @staticmethod
    def get_service(agency):
        if agency == 'chicago-cta-bus':
            return ChicagoCTABusService()
        if agency == 'chicago-cta-train':
            return ChicagoCTATrainService()
        if agency == 'austin-metro-bus':
            return AustinMetroBusService()
        if agency == 'sf-muni-bus':
            return SanFranciscoMuniBusService()
        return None
