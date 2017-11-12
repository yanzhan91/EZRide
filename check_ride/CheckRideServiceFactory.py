from ChicagoCTABusService import ChicagoCTABusService
from ChicagoCTATrainService import ChicagoCTATrainService
from AustinMetroBusService import AustinMetroBusService
from SanFranciscoMuniBusService import SanFranciscoMuniBusService
from LosAngelesMetroBusService import LosAngelesMetroBusService


class CheckRideServiceFactory(object):

    @staticmethod
    def get_service(agency):
        if agency == 'chicago-cta-bus':
            return ChicagoCTABusService()
        if agency == 'chicago-cta-train':
            return ChicagoCTATrainService()
        if agency == 'austin-metro-bus':
            return AustinMetroBusService()
        if agency == 'sanfrancisco-muni-bus':
            return SanFranciscoMuniBusService()
        if agency == 'losangeles-metro-bus':
            return LosAngelesMetroBusService()
        return None
