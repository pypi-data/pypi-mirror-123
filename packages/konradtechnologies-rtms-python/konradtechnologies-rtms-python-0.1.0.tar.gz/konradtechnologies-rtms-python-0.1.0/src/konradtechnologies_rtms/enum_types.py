from enum import Enum


class RtmsStringEnum(Enum):
    def __str__(self):
        return self.name


class RtmsSystemStatus(RtmsStringEnum):
    """
    An enum type of the RTMS system status.  (Ready, Not Ready, or in Warmup)
    """
    NOTREADY = "NOTREADY"
    READY = "READY"
    WARMUP = "WARMUP"


class RtmsTriggerEdge(RtmsStringEnum):
    RISING = "RISING"
    FALLING = "FALLING"


class RtmsAveragingType(RtmsStringEnum):
    MEAN = "MEAN"
    MAX = "MAX"


class RtmsEVMModulationType(RtmsStringEnum):
    ASK = "ASK"
    FSK = "FSK"
    PSK = "PSK"
    QAM = "QAM"
    MSK = "MSK"


class RtmsEVMPSKFormat(RtmsStringEnum):
    NORMAL = "NORMAL"
    OFFSET_QPSK = "OFFSETQPSK"
    PI4_QPSK = "PI4_QPSK"
    PI8_8PSK = "PI8_8PSK"
    THREE_PI8_8PSK = "3PI8_8PSK"
