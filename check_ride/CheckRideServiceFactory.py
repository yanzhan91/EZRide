from ChicagoCTABusService import ChicagoCTABusService
from ChicagoCTATrainService import ChicagoCTATrainService
from AustinMetroBusService import AustinMetroBusService
from SanFranciscoMuniBusService import SanFranciscoMuniBusService
from LosAngelesMetroBusService import LosAngelesMetroBusService
from PortlandTriMetBusService import PortlandTriMetBusService


class CheckRideServiceFactory(object):

    @staticmethod
    def get_service(agency):
        if agency == 'chicago-cta-bus':
            return ChicagoCTABusService()
        if agency == 'chicago-cta-train':
            return ChicagoCTATrainService()
        if agency == 'austin-metro-bus':
            return AustinMetroBusService()
        if agency == 'san-francisco-muni-bus':
            return SanFranciscoMuniBusService()
        if agency == 'los-angeles-metro-bus':
            return LosAngelesMetroBusService()
        if agency == 'portland-tri-met-bus':
            return PortlandTriMetBusService()
        return None
