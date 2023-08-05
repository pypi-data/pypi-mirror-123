from packaging.version import Version

from konradtechnologies_rtms.communication import base_communication
from konradtechnologies_rtms.target import RadarTarget
from konradtechnologies_rtms.enum_types import *


class RtmsScpiCommunication(base_communication.RtmsBaseCommunication):
    def get_system_status(self):
        return self._query_and_check_response("STATUS?")

    def set_radar_targets(self, targets):
        if self.rtms_version.major == 2:
            self._set_radar_targets_v2(targets)
        else:
            self._set_radar_targets_v3(targets)

    def _set_radar_targets_v2(self, targets):
        self._query_and_check_response("TARGET:SETNUMTARGETS {}".format(len(targets)))

        for i in range(0, len(targets)):
            self._query_and_check_response("TARGET:RANGE:VALUE {} {}".format(i+1, targets[i].distance))
            self._query_and_check_response("TARGET:RCS:VALUE {} {}".format(i+1, targets[i].rcs))
            self._query_and_check_response("TARGET:VELOCITY {} {}".format(i+1, targets[i].velocity))
            self._query_and_check_response("TARGET:ANGLE {} {} {}".format(i+1, targets[i].azimuth,
                                                                          targets[i].elevation))

    def _set_radar_targets_v3(self, targets):
        param_string = ''

        for target in targets:
            param_string += " {} {} {} {} {}".format(target.distance, target.rcs, target.velocity, target.azimuth,
                                                     target.elevation)
        self._query_and_check_response("TARGET:SETALL{}".format(param_string))

    def get_radar_targets(self):
        if self.rtms_version <= Version('3.0.0b2'):
            targets = self._get_radar_targets_v2()
        else:
            targets = self._get_radar_targets_v3()

        return targets

    def _get_radar_targets_v2(self):
        number_targets = int(self._query_and_check_response("TARGET:TOTALTARGETS?"))

        radar_targets = []
        for i in range(1, number_targets + 1):
            target_distance = float(self._query_and_check_response("TARGET:RANGE:VALUE? {}".format(i)))
            target_rcs = float(self._query_and_check_response("TARGET:RCS:VALUE? {}".format(i)))
            target_velocity = float(self._query_and_check_response("TARGET:VELOCITY? {}".format(i)))
            response_angle = self._query_and_check_response("TARGET:ANGLE? {}".format(i))
            target_azimuth = response_angle.split(" ")[0]
            target_elevation = response_angle.split(" ")[1]

            new_target = RadarTarget(distance=target_distance,
                                     rcs=target_rcs,
                                     velocity=target_velocity,
                                     azimuth=target_azimuth,
                                     elevation=target_elevation)

            radar_targets.append(new_target)

        return radar_targets

    def _get_radar_targets_v3(self):
        response = self._query_and_check_response("TARGET:GETALL?")
        parsed_target_parameters = response.split(" ")

        radar_targets = []
        for i in range(0, len(parsed_target_parameters) - 1, 5):
            new_target = RadarTarget(distance=parsed_target_parameters[i],
                                     rcs=parsed_target_parameters[i + 1],
                                     velocity=parsed_target_parameters[i + 2],
                                     azimuth=parsed_target_parameters[i + 3],
                                     elevation=parsed_target_parameters[i + 4])

            radar_targets.append(new_target)

        return radar_targets

    def configure_system(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'setup_distance':
                self._query_and_check_response("SYSTEM:ANTDIST {}".format(value))
            elif key == 'antenna_gain_rx':
                self._query_and_check_response("SYSTEM:ANTGAINRX {}".format(value))
            elif key == 'antenna_gain_tx':
                self._query_and_check_response("SYSTEM:ANTGAINTX {}".format(value))
            elif key == 'center_frequency':
                self._query_and_check_response("SYSTEM:CENTERFREQUENCY {}".format(value))
            elif key == 'sensor_eirp':
                self._query_and_check_response("SYSTEM:EXPECTEDEIRP {}".format(value))
            else:
                raise KeyError('Invalid keyword argument: "{}"'.format(key))

    def configure_trigger(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'enabled':
                self._query_and_check_response("MEASUREMENT:CONFIGURATION:TRIGGER:ENABLED {}".format(int(value)))
            elif key == 'level':
                self._query_and_check_response("MEASUREMENT:CONFIGURATION:TRIGGER:LEVEL {}".format(value))
            elif key == 'edge':
                self._query_and_check_response("MEASUREMENT:CONFIGURATION:TRIGGER:EDGE {}".format(value))
            elif key == 'pretrig_samples':
                self._query_and_check_response("MEASUREMENT:CONFIGURATION:TRIGGER:PRETRIGSAMPLES {}".format(value))
            elif key == 'quiet_time':
                self._query_and_check_response("MEASUREMENT:CONFIGURATION:TRIGGER:QUIETTIME {}".format(value))
            elif key == 'timeout':
                self._query_and_check_response("MEASUREMENT:CONFIGURATION:TRIGGER:TIMEOUT {}".format(value))
            else:
                raise KeyError('Invalid keyword argument: "{}"'.format(key))

    def configure_averaging(self, enabled=False, count=1, averaging_type=RtmsAveragingType.MEAN):
        if not enabled:
            self._query_and_check_response("MEASUREMENT:CONFIGURATION:AVG:TYPE NONE")
        else:
            self._query_and_check_response("MEASUREMENT:CONFIGURATION:AVG:TYPE {}".format(averaging_type))
            self._query_and_check_response("MEASUREMENT:CONFIGURATION:AVG:COUNT {}".format(count))

    def set_active_measurements(self, eirp=False, obw=False, linearity=False, phasenoise=False, evm=False):
        self._query_and_check_response("MEASUREMENT:ACTIVE:EIRP {}".format(int(eirp)))
        self._query_and_check_response("MEASUREMENT:ACTIVE:OBW {}".format(int(obw)))
        self._query_and_check_response("MEASUREMENT:ACTIVE:LINEARITY {}".format(int(linearity)))
        self._query_and_check_response("MEASUREMENT:ACTIVE:PHASENOISE {}".format(int(phasenoise)))
        self._query_and_check_response("MEASUREMENT:ACTIVE:EVM {}".format(int(evm)))

    def set_measurement_duration(self, duration: float):
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:DURATION {}".format(duration))

    def get_measurement_duration(self):
        return float(self._query_and_check_response("MEASUREMENT:CONFIGURATION:DURATION?"))

    def set_measurement_rbw(self, rbw: float):
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:RBW {}".format(rbw))

    def get_measurement_rbw(self):
        return float(self._query_and_check_response("MEASUREMENT:CONFIGURATION:RBW?"))

    def initiate_measurement(self, wait_until_complete=True):
        self._query_and_check_response("MEASUREMENT:START")
        if wait_until_complete:
            self._query_and_check_response("*OPC?")

    def configure_measurement_obw_percent(self, percent=98):
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:OBW:METHOD PERCENTAGE")
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:OBW:PERCENTAGE {}".format(percent))

    def configure_measurement_obw_xdb(self, x_db=-26):
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:OBW:METHOD XDB")
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:OBW:XDB {}".format(x_db))

    def configure_measurement_phasenoise(self, offset_frequencies=[1E3, 10E3, 100E3, 1E6]):
        offset_frequency_list = ''

        for frequency in offset_frequencies:
            offset_frequency_list += " {}".format(frequency)

        self._query_and_check_response("MEASUREMENT:CONFIGURATION:PHASENOISE:OFFSETFREQUENCIES{}"
                                       .format(offset_frequency_list))

    def configure_measurement_evm(self, modulation_type=RtmsEVMModulationType.PSK, mary=4, symbol_rate=100E3,
                                  differential=False, psk_format=RtmsEVMPSKFormat.NORMAL):
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:EVM:MODULATIONTYPE {}".format(modulation_type))
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:EVM:MARY {}".format(mary))
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:EVM:SYMBOLRATE {}".format(symbol_rate))
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:EVM:DIFFERENTIAL {}".format(int(differential)))
        self._query_and_check_response("MEASUREMENT:CONFIGURATION:EVM:PSKFORMAT {}".format(psk_format))

    def get_measurement_results_eirp(self):
        results = dict()
        results['avg'] = float(self._query_and_check_response("MEASUREMENT:EIRP:AVG?"))
        results['dutycycle'] = float(self._query_and_check_response("MEASUREMENT:EIRP:DUTYCYCLE?"))
        results['min'] = float(self._query_and_check_response("MEASUREMENT:EIRP:MIN?"))
        results['period'] = float(self._query_and_check_response("MEASUREMENT:EIRP:PERIOD?"))
        results['pk'] = float(self._query_and_check_response("MEASUREMENT:EIRP:PK?"))
        results['pulseduration'] = float(self._query_and_check_response("MEASUREMENT:EIRP:PULSEDURATION?"))

        return results

    def get_measurement_results_obw(self):
        results = dict()
        results['bandwidth'] = float(self._query_and_check_response("MEASUREMENT:OBW:BANDWIDTH?"))
        results['center_frequency'] = float(self._query_and_check_response("MEASUREMENT:OBW:CENTERFREQUENCY?"))

        return results

    def get_measurement_results_linearity(self):
        results = dict()
        results['duration'] = float(self._query_and_check_response("MEASUREMENT:LINEARITY:DURATION?"))
        results['max_freq'] = float(self._query_and_check_response("MEASUREMENT:LINEARITY:MAXFREQ?"))
        results['min_freq'] = float(self._query_and_check_response("MEASUREMENT:LINEARITY:MINFREQ?"))
        results['slope'] = float(self._query_and_check_response("MEASUREMENT:LINEARITY:SLOPE?"))

        return results

    def get_measurement_results_phasenoise(self):
        results = dict()
        raw_results = self._query_and_check_response("MEASUREMENT:PHASENOISE:RAWRESULTS?").split(" ")

        raw_results_dict = dict()
        for i in range(0, len(raw_results), 2):
            raw_results_dict[float(raw_results[i])] = float(raw_results[i+1])

        fitted_results = self._query_and_check_response("MEASUREMENT:PHASENOISE:FITTEDRESULTS?").split(" ")

        fitted_results_dict = dict()
        for i in range(0, len(raw_results), 2):
            fitted_results_dict[float(fitted_results[i])] = float(fitted_results[i + 1])

        results["raw_results"] = raw_results_dict
        results["fitted_results"] = fitted_results_dict

        return results

    def get_measurement_results_evm(self):
        results = dict()
        results['evm_avg'] = float(self._query_and_check_response("MEASUREMENT:EVM:AVG??"))
        results['evm_max'] = float(self._query_and_check_response("MEASUREMENT:EVM:MAX??"))
        results['mer'] = float(self._query_and_check_response("MEASUREMENT:EVM:MER??"))
        results['freq_drift'] = float(self._query_and_check_response("MEASUREMENT:EVM:FREQDRIFT??"))
        results['freq_offset'] = float(self._query_and_check_response("MEASUREMENT:EVM:FREQOFFSET??"))
        results['demod_bits'] = float(self._query_and_check_response("MEASUREMENT:EVM:DEMODBITS??"))

        return results

    def _query_and_check_response(self, cmd):
        response = self.query(cmd)
        return self._parse_and_check_response(response)

    def _parse_and_check_response(self, response):
        if "OK" not in response:
            raise base_communication.RtmsCmdError("RTMS Response: {}".format(response))

        return response.split(" OK")[0]
