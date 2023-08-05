from konradtechnologies_rtms.enum_types import RtmsAveragingType, RtmsEVMModulationType, RtmsEVMPSKFormat


class RtmsCommandSet(object):
    """
    The purpose of this class is to provide an interface and define all appropriate commands available for
    communication to KT-RTMS.  No implementation of any command takes place in this class.  Each of these
    methods should be overridden in the specific communication class.
    """
    def get_rtms_version(self):
        raise NotImplementedError()

    def get_system_status(self):
        raise NotImplementedError()

    def set_radar_targets(self, targets):
        raise NotImplementedError()

    def get_radar_targets(self):
        raise NotImplementedError()

    def configure_system(self, **kwargs):
        raise NotImplementedError()

    def configure_trigger(self, **kwargs):
        raise NotImplementedError()

    def configure_averaging(self, enabled=False, count=1, averaging_type=RtmsAveragingType.MEAN):
        raise NotImplementedError()

    def set_active_measurements(self, eirp=False, obw=False, linearity=False, phasenoise=False, evm=False):
        raise NotImplementedError()

    def set_measurement_duration(self, duration: float):
        raise NotImplementedError()

    def get_measurement_duration(self):
        raise NotImplementedError()

    def set_measurement_rbw(self, rbw: float):
        raise NotImplementedError()

    def get_measurement_rbw(self):
        raise NotImplementedError()

    def configure_measurement_obw_percent(self, percent=98):
        raise NotImplementedError()

    def configure_measurement_obw_xdb(self, x_db=-26):
        raise NotImplementedError()

    def configure_measurement_phasenoise(self, offset_frequencies=[1E3, 10E3, 100E3, 1E6]):
        raise NotImplementedError()

    def configure_measurement_evm(self, modulation_type=RtmsEVMModulationType.PSK, mary=4, symbol_rate=100E3,
                                  differential=False, psk_format=RtmsEVMPSKFormat.NORMAL):
        raise NotImplementedError()

    def initiate_measurement(self, wait_until_complete=True):
        raise NotImplementedError()

    def get_measurement_results_eirp(self):
        raise NotImplementedError()

    def get_measurement_results_obw(self):
        raise NotImplementedError()

    def get_measurement_results_linearity(self):
        raise NotImplementedError()

    def get_measurement_results_phasenoise(self):
        raise NotImplementedError()

    def get_measurement_results_evm(self):
        raise NotImplementedError()
