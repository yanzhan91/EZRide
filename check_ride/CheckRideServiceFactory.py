from ChicagoCTABusService import ChicagoCTABusService
from ChicagoCTATrainService import ChicagoCTATrainService
from AustinMetroBusService import AustinMetroBusService
from SanFranciscoMuniBusService import SanFranciscoMuniBusService
from LosAngelesMetroBusService import LosAngelesMetroBusService
from PortlandTriMetBusService import PortlandTriMetBusService
from DCMetroBusService import DCMetroBusService


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
        if agency == 'portland-tri-met-bus':
            return PortlandTriMetBusService()
        if agency == 'dc-metro-bus':
            return DCMetroBusService()
        return None
