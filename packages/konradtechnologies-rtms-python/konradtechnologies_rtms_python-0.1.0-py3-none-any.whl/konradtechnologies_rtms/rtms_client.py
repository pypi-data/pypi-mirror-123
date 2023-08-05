import time
from packaging.version import Version

from konradtechnologies_rtms.communication import base_communication, scpi_communication
from konradtechnologies_rtms.enum_types import *
from konradtechnologies_rtms.target import RadarTarget, DynamicRadarTarget


class RtmsClient(object):
    """
    Provides an interface to control the KT-RTMS software.  The KT-RTMS must be running on the host computer
    and ready to accept a remote connection.
    """
    def __init__(self, ip_address="127.0.0.1", port=6000, timeout=10):
        """
        Creates an object of the RtmsClient class to communicate with RTMS

        :param ip_address: The IP address of the host computer running KT-RTMS
        :type ip_address: str
        :param port: TCP/IP port which KT-RTMS is listening on.  The default port is 6000.
        :type port: int
        :param timeout: TCP/IP timeout for receiving a response for each command.
        :type timeout: int
        """
        self.communication = base_communication.RtmsBaseCommunication(ip_address, port, timeout)
        self.rtms_version = None

    def connect(self):
        """
        Initiates a connection to KT-RTMS.  Automatically checks the connection by querying the KT-RTMS version.

        """
        self.communication.connect()
        # Get the RTMS version to be able to select a communication method
        self.rtms_version = self.communication.get_rtms_version()

        # This section of code allows for different communication methods, depending on the version of RTMS running.
        # If in the future, the communication protocol changes, one should implement a new communication class
        # and define it here, based on the RTMS version.

        if self.rtms_version.major == 1:
            # KT-RTMS Version 1.x ==> Not supported
            raise base_communication.RtmsInstError("This version of RTMS is not supported by package")
        else:
            # KT-RTMS Version 2.x+ ==> Use SCPI communication
            # Make the communication use SCPI communication by type-casting to SCPI communication class
            self.communication.__class__ = scpi_communication.RtmsScpiCommunication

    def disconnect(self):
        """
        Disconnects from KT-RTMS
        """
        self.communication.disconnect()

    def get_rtms_version(self):
        """
        Returns the RTMS version which is connected.

        :return: The version of RTMS as a packaging.version object.
        :rtype: Version
        """
        return self.rtms_version

    def get_rtms_version_string(self):
        """
        Returns the RTMS version which is connected, as a string.

        :return: The version of RTMS as a string.
        :rtype: str
        """
        return str(self.rtms_version)

    def get_system_status(self):
        """
        Fetches the current system status

        :return: The current system status (if the system is running and warmed up)
        :rtype: RtmsSystemStatus
        """
        return self.communication.get_system_status()

    def set_radar_targets(self, targets):
        """
        Configures a set of radar targets for RTMS to simulate.  Note that only minimal error checking is done on the
        list of targets.  As a result, not all targets may be simulated if the system is unable to simulate all
        requested targets

        :param targets: An array of radar targets to be simulated
        :type targets: list[RadarTarget]
        """
        self.communication.set_radar_targets(targets)

    def set_dynamic_range_targets(self, dynamic_targets, time_interval=0.1):
        """
        Executes a dynamic target script.  Note that the timing of execution is handled solely by Python.  As such,
        jitter and latency may occur.  If precise timing is required, this function should not be used.

        :param dynamic_targets: A list of dynamic targets to execute.  The outer list is for each simulated object.
            The inner list is a set of dynamic targets to execute, one after another.
        :type dynamic_targets: list[list[DynamicRadarTarget]]
        :param time_interval: The interval of time to determine individual Radar Target points, in sec.
        :type time_interval: float
        """
        individual_points = list()
        number_targets = len(dynamic_targets)
        target_list = list()

        target_number = 0
        max_length = 0

        # Loop through each target which was sent
        for object_dynamic_targets in dynamic_targets:
            # Create an empty list object that will be populated below
            individual_points.append(list())
            # The target list is used during the timed loop, initializing with a default RadarTarget object
            target_list.append(RadarTarget())

            # Loop through each dynamic target sent
            for dynamic_target in object_dynamic_targets:
                individual_points[target_number].extend(dynamic_target.get_target_points(time_interval=time_interval))

            # Keep track if this list is the longest object list
            if len(individual_points[target_number]) > max_length:
                max_length = len(individual_points[target_number])

            # Increment target number
            target_number = target_number + 1

        last_time = time.time()
        for i in range(0, max_length):
            # Get individual targets

            for target_number in range(0, number_targets):
                # Try to find the individual point for this specific time instance.  if the index is out of range,
                # that means that target is done (but another target is still going).  Just hold the last value.
                try:
                    target_list[target_number] = individual_points[target_number][i]
                except IndexError:
                    # Keep the last target point, but change velocity to zero since that target is now stationary
                    target_list[target_number].velocity = 0
                    pass

            self.set_radar_targets(target_list)
            # Sleep until the next iteration
            time_to_sleep = time_interval - (time.time() - last_time)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
            last_time = time.time()

        # Set all targets as static objects now that the script is complete
        for target_number in range(0, number_targets):
            target_list[target_number].velocity = 0
        self.set_radar_targets(target_list)

    def get_radar_targets(self):
        """
        Fetches the list of radar targets from RTMS.
        Note that this function returns a different list of targets based on the version of RTMS:

        *RTMS 2.x* - Returns the list of radar targets which have been requested.

        *RTMS 3.x+* - Returns the list of radar targets which are actually being simulated.  Note that the size of
        this array may be different than the requested radar target list if the entire list could not be
        simulated

        :return: An array of radar targets
        :rtype: list[RadarTarget]
        """
        return self.communication.get_radar_targets()

    def configure_system(self, **kwargs):
        """
        Configures overall system parameters.

        :key setup_distance (float): Distance between the RTS radio head and the sensor, in meters.
        :key antenna_gain_rx (float): TX antenna gain of the RTS radio head, in dBi.
        :key antenna_gain_tx (float): RX antenna gain of the RTS radio head, in dBi.
        :key center_frequency (float): Sensor center frequency, in Hz.
        :key sensor_eirp (float): Expected EIRP of the sensor (used to set reference level of instrument), in dBm.
        """
        self.communication.configure_system(**kwargs)

    def configure_trigger(self, **kwargs):
        """
        Configures the RF trigger for RF measurements

        :key enabled (boolean): Configures if an RF trigger is enabled.  If disabled, the measurement acts like an
            immediate trigger.
        :key level (float): The trigger level, in dBm
        :key edge (RtmsTriggerEdge): Defines the edge to trigger on at the level specified
        :key pretrig_samples (int): How many pre-trigger samples are included in the acquisition.
        :key quiet_time (float): The amount of time which the RF signal signal is above or below the trigger level,
            prior to triggering, in seconds.  ie, if the trigger level is defined as a rising edge, the quiet_time
            is the amount of time where the signal is /below/ the trigger level, prior to a rising edge trigger.
        :key timeout (float): The amount of time that the RF measurement waits for a trigger, in seconds.
        """
        self.communication.configure_trigger(**kwargs)

    def configure_averaging(self, enabled=False, count=1, averaging_type=RtmsAveragingType.MEAN):
        """
        Configures the averging parameters used during RF measurements.

        :param enabled: Specifies if averaging is enabled
        :type enabled: bool
        :param count: If averaging is enabled, defines the number of RF measurements included in the average
        :type count: int
        :param averaging_type: If averaging is enabled, defines the type of average ("mean" or "max")
        :type averaging_type: RtmsAveragingType
        """
        self.communication.configure_averaging(enabled=enabled, count=count, averaging_type=averaging_type)

    def set_active_measurements(self, eirp=False, obw=False, linearity=False, phasenoise=False, evm=False):
        """
        Sets the active RF measurements to perform.  Setting individual RF measurements on/off can improve measurement
        time

        :param eirp: Defines if the EIRP measurement is enabled
        :type eirp: bool
        :param obw: Defines if the occupied bandwidth measurement is enabled
        :type obw: bool
        :param linearity: Defines if the linearity measurement is enabled
        :type linearity: bool
        :param phasenoise: Defines if the phase noise measurement is enabled
        :type phasenoise: bool
        :param evm: Defines if the EVM (error vector magnitude) measurement is enabled
        :type evm: bool
        """
        self.communication.set_active_measurements(eirp, obw, linearity, phasenoise, evm)

    def set_measurement_duration(self, duration):
        """
        Sets the duration of the RF measurement.  Note that changing this parameter will affect
        the measurement resolution bandwidth as the sample rate of the measurement is fixed.

        :param duration: Duration of the RF measurement, in seconds.
        :type duration: float
        """
        self.communication.set_measurement_duration(duration)

    def get_measurement_duration(self):
        """
        Gets the duration of the RF measurement

        :return: Duration of the RF measurement, in seconds
        :rtype: float
        """
        return self.communication.get_measurement_duration()

    def set_measurement_rbw(self, rbw):
        """
        Sets the resolution bandwidth (RBW) of the RF measurement.  Note that changing this parameter will affect
        the measurement duration as the sample rate of the measurement is fixed.

        :param rbw: The resolution bandwidth of the RF measurement, in Hz.
        :type rbw: int
        """
        self.communication.set_measurement_rbw(rbw)

    def get_measurement_rbw(self):
        """
        Gets the resolution bandwidth (RBW) of the RF measurement.

        :return: The resolution bandwidth of the RF measurement, in Hz.
        :rtype: int
        """
        return self.communication.get_measurement_rbw()

    def configure_measurement_obw_percent(self, percent=98):
        """
        Configures the OBW measurement in percent of power mode, with the specified percent.  In this mode, the
        system computes the occupied bandwidth as the bandwidth where x% of all power is present.

        :param percent: The percent of power to define the occupied bandwidth
        :type percent: float
        """
        self.communication.configure_measurement_obw_percent(percent=percent)

    def configure_measurement_obw_xdb(self, x_db=-26):
        """
        Configures the OBW measurement in xdB mode, with the specified parameter.  In this mode, the system computes
        the occupied bandwidth as the bandwidth where the power is x dB down from the peak power in the spectrum.

        :param x_db: The amount of power down from the peak power to define the occupied bandwidth, in dB.
        :type x_db: float
        """
        self.communication.configure_measurement_obw_xdb(x_db=x_db)

    def configure_measurement_phasenoise(self, offset_frequencies=[1E3, 10E3, 100E3, 1E6]):
        """
        Configures the offset frequencies to measure during the phase noise measurement.

        :param offset_frequencies: An array of offset frequencies to measure, in Hz.
        :type offset_frequencies: list[float]
        """
        self.communication.configure_measurement_phasenoise(offset_frequencies=offset_frequencies)

    def configure_measurement_evm(self, modulation_type=RtmsEVMModulationType.PSK, mary=4, symbol_rate=100E3,
                                  differential=False, psk_format=RtmsEVMPSKFormat.NORMAL):
        """
        Configures the EVM measurement.

        :param modulation_type: The modulation type of the radar signal to be analyzed.  Types allowed are "ask", "fsk",
            "psk", "qam", or "msk".
        :type modulation_type: RtmsEVMModulationType
        :param mary: Sets the M-ary of the modulated signal.  Valid numbers are powers of two.  (For example, QPSK is
            4 M-ary.  16-QAM is 16 M-ary).
        :type mary: int
        :param symbol_rate: Sets the symbol rate of the modulated signal to be used during de-modulation.
        :type symbol_rate: float
        :param differential: Sets if teh signal to be de-modulated is a differentially modulated signal (ie, DQPSK)
        :type differential: bool
        :param psk_format: Sets the type of PSK modulation to be used.  This parameter is only used if the modulation
            type is set to "psk".  Available psk formats are "normal", "offsetqpsk", pi4_qpsk", "pi8_8psk", "3pi8_8psk"
        :type psk_format: RtmsEVMPSKFormat
        """
        self.communication.configure_measurement_evm(modulation_type=modulation_type, mary=mary,
                                                     symbol_rate=symbol_rate, differential=differential,
                                                     psk_format=psk_format)

    def initiate_measurement(self, wait_until_complete=True):
        """
        Initiates an RF measurement.  Optionally blocks until the measurement is complete and all results are ready.

        :param wait_until_complete: If True, this method blocks until the measurement is complete.  If False, this
            method returns immediately.
        :type wait_until_complete: bool
        """
        self.communication.initiate_measurement(wait_until_complete)

    def get_measurement_results_eirp(self):
        """
        Retrieves the results of the EIRP measurement.  These results are only valid if the EIRP test was enabled prior
        to initiating the measurement.

        :return: A dictionary of EIRP results.
        :rtype: dict
        """
        return self.communication.get_measurement_results_eirp()

    def get_measurement_results_obw(self):
        """
        Retrieves the results of the OBW measurement.  These results are only valid if the OBW test was enabled prior
        to initiating the measurement.

        :return: A dictionary of OBW results.
        :rtype: dict
        """
        return self.communication.get_measurement_results_obw()

    def get_measurement_results_linearity(self):
        """
        Retrieves the results of the linearity measurement.  These results are only valid if the linearity test was
        enabled prior to initiating the measurement.

        :return: A dictionary of linearity results.
        :rtype: dict
        """
        return self.communication.get_measurement_results_linearity()

    def get_measurement_results_phasenoise(self):
        """
        Retrieves the results of the phase noise measurement.  These results are only valid if the phase noise test was
        enabled prior to initiating the measurement.

        :return: A dictionary of phase noise results.
        :rtype: dict
        """
        return self.communication.get_measurement_results_phasenoise()

    def get_measurement_results_evm(self):
        """
        Retrieves the results of the EVM measurement.  These results are only valid if the EVM test was enabled prior
        to initiating the measurement.

        :return: A dictionary of EVM results.
        :rtype: dict
        """
        return self.communication.get_measurement_results_evm()
