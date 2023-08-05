import socket
import ipaddress
from packaging.version import Version, parse as version_parse
from konradtechnologies_rtms.communication.command_set import RtmsCommandSet


class RtmsBaseCommunication(RtmsCommandSet):
    """
    Implements the base communication structure for communicating to KT-RTMS.  It is intended that this class only
    implement a single command to fetch the RTMS version.  After querying the software version, the RTMS client should
    cast this class to a more specific class, depending on the communication to be used.
    """
    cmd_terminator = '\n'
    response_terminator = '\n'

    def __init__(self, ip_address, port=6000, timeout=10, no_delay=True):
        """
        Open socket connection with settings for instrument control.

        :param ip_address: Instrument host IP address. Argument is a string containing a valid IP address.
        :type ip_address: str
        :param port: Port used by the instrument to facilitate socket communication (KT-RTMS uses port 6000 by
            default).
        :type port: int
        :param timeout: Timeout in seconds.
        :type port: int
        :param no_delay: True sends data immediately without concatenating multiple packets together. Just leave
            this alone.
        :type no_delay: bool
        """
        # Validate IP address (will raise an error if given an invalid address).
        ipaddress.ip_address(ip_address)

        self.ip_address = ip_address
        self.port = port

        # Create socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Handle
        if no_delay:
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # Turn blocking behavior off so we can control the socket while it processes commands
        self.socket.setblocking(False)
        # Set timeout
        self.socket.settimeout(timeout)

        # Reserve the class variable for the RTMS software version
        self.rtms_version = None

    def connect(self):
        """
        Connects to the socket
        """
        # Connect to socket
        self.socket.connect((self.ip_address, self.port))

        # Read version to ensure communication
        self.rtms_version = self.get_rtms_version()

    def disconnect(self):
        """
        Gracefully close socket connection.
        """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def write(self, cmd):
        """
        Writes a command to the instrument.  A termination character, if defined, will be added to the end of the
        string.

        :param cmd: command to be sent to the instrument.
        :type cmd: str
        """

        if not isinstance(cmd, str):
            raise RtmsInstError('Argument must be a string.')

        msg = '{}{}'.format(cmd, self.cmd_terminator)

        self.socket.send(msg.encode('latin_1'))

    def read(self):
        """
        Reads the output buffer of the instrument.  The termination character will be removed from the string.

        :return: Contents of the instrument's output buffer.
        :rtype: str
        """

        response = b''
        while response[-1:] != self.response_terminator.encode('latin_1'):
            response += self.socket.recv(1024)

        # Strip out whitespace and return.
        return response.decode('latin_1').strip()

    def query(self, cmd):
        """
        Sends query to instrument and reads the output buffer immediately afterward.

        :param cmd: Query to be sent to instrument (should end in a "?" character).
        :type cmd: str
        :return: Response from instrument's output buffer as a latin_1-encoded string.
        :rtype: str
        """

        if not isinstance(cmd, str):
            raise RtmsInstError('Argument must be a string.')

        self.write(cmd)
        return self.read()

    def get_rtms_version(self):
        """
        Queries the version of RTMS.  To be able to fetch the version regardless of the communication scheme,
        this command should be implemented in every version.

        :return: The version of RTMS as a packaging.version object.
        :rtype: Version
        """
        # *IDN? is implemented in all version of RTMS to determine version information
        # Example reply: "Konrad Technologies,KT-RTMS,,3.0.0b2 OK"
        idn_response = self.query('*IDN?')

        parsed_idn = idn_response.split(",")

        if parsed_idn[1] != "KT-RTMS":
            raise RtmsInstError('Instrument did not respond with valid identification')

        # TODO: Catch failed version number
        parsed_version = version_parse(parsed_idn[3].split(" ")[0])

        return parsed_version


class RtmsInstError(Exception):
    """
    A RtmsInstError is thrown when there is an error communicating to the RTMS software.
    (ie, a connection issue occurs)
    """
    pass


class RtmsCmdError(Exception):
    """
    A RtmsCmdError is thrown when a command fails when communicating to the RTMS software.
    (ie, the command was sent successfully to the instrument, but the instrument reported the parameters were invalid)
    """
    pass
