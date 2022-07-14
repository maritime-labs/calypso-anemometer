# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from enum import Enum


class NetworkProtocol(Enum):
    TCP = "tcp"
    UDP = "udp"


class NetworkProtocolMode(Enum):
    UNICAST = "unicast"
    BROADCAST = "broadcast"
    MULTICAST = "multicast"


class TelemetryProtocol(Enum):
    UDP_SIGNALK_DELTA = "udp+signalk+delta"
    UDP_BROADCAST_NMEA0183 = "udp+broadcast+nmea0183"
