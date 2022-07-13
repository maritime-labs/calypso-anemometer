from enum import Enum


class NetworkProtocol(Enum):
    TCP = "tcp"
    UDP = "udp"


class TelemetryProtocol(Enum):
    UDP_SIGNALK_DELTA = "udp+signalk+delta"
