# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
"""
About
=====

NMEA-0183 over TCP or UDP.


Network transport
=================

The default port for UDP is 10110. Port 10110 is
designated by IANA for "NMEA-0183 Navigational Data".


Message format
==============

The NMEA-0183 sentence information for "relative wind"
``VWR - Relative Wind Speed and Angle``::

             1  2  3  4  5  6  7  8 9
             |  |  |  |  |  |  |  | |
     $--VWR,x.x,a,x.x,N,x.x,M,x.x,K*hh<CR><LF>

     Field Number:
      1) Wind direction magnitude in degrees
      2) Wind direction Left/Right of bow
      3) Speed
      4) N = Knots
      5) Speed
      6) M = Meters Per Second
      7) Speed
      8) K = Kilometers Per Hour
      9) Checksum

-- http://www.nmea.de/nmea0183datensaetze.html


CLI sender / receiver
=====================

Submit and receive NMEA-0183 over UDP broadcast on the command line.

::

    # Submit
    echo '$IIVWR,045.0,L,12.6,N,6.5,M,23.3,K*52' | socat -u -t5 - udp-datagram:openplotter.local:2000,broadcast

    # Receive
    socat -u udp4-recvfrom:2000,reuseaddr,fork system:cat
    nc -lu 10.10.10.255 2000
"""
import dataclasses
import logging
import typing as t

from calypso_anemometer.model import CalypsoReading
from calypso_anemometer.telemetry import NetworkProtocol, NetworkProtocolMode, NetworkTelemetry

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Nmea0183GenericMessage:
    """
    Represent and serialize generic NMEA-0183 message.
    """

    identifier: str
    fields: t.List[t.Union[t.AnyStr, t.SupportsInt, t.SupportsFloat, None]]

    def render(self):
        parts = [self.identifier] + self.fields
        parts = [part is not None and str(part) or "" for part in parts]
        message = ",".join(parts)
        return message


@dataclasses.dataclass
class Nmea0183MessageIIVWR:
    """
    Represent and serialize NMEA-0183 IIVWR message.

    VWR - Relative Wind Speed and Angle
    """

    IDENTIFIER = "$IIVWR"
    direction_magnitude_in_degrees: t.Optional[float] = None
    direction_left_right_of_bow: t.Optional[str] = None
    speed_knots: t.Optional[float] = None
    speed_meters_per_second: t.Optional[float] = None
    speed_kilometers_per_hour: t.Optional[float] = None

    def to_message(self):
        """
        Factory for generic `Nmea0183Message`.

        TODO: Derive individual values from others.
              - Compute `direction_left_right_of_bow` from `direction_magnitude_in_degrees`.
              - Compute missing `speed_` from other `speed_` values.
        """
        return Nmea0183GenericMessage(
            identifier=self.IDENTIFIER,
            fields=[
                self.convert_value(self.direction_magnitude_in_degrees),
                self.direction_left_right_of_bow,
                self.convert_value(self.speed_knots),
                "N",
                self.convert_value(self.speed_meters_per_second),
                "M",
                self.convert_value(self.speed_kilometers_per_hour),
                "K",
            ],
        )

    @staticmethod
    def convert_value(value, converter=float, default=""):
        if value is None:
            value = default
        else:
            value = converter(value)
        return value


@dataclasses.dataclass
class Nmea0183Messages:
    """
    Represent and render a list of NMEA-0183 messages.
    """

    items: t.Optional[t.List[Nmea0183GenericMessage]] = None

    def set_reading(self, reading: CalypsoReading):
        """
        Derive NMEA-0183 IIVWR message from measurement reading.
        """
        self.items = [
            Nmea0183MessageIIVWR(
                direction_magnitude_in_degrees=abs(reading.wind_direction_180),
                direction_left_right_of_bow=reading.wind_left_right_indicator,
                speed_meters_per_second=reading.wind_speed,
            ).to_message()
        ]

    def aslist(self):
        """
        Render measurement items to multiple NMEA-0183 sentences.
        """
        messages = [item.render() for item in self.items]
        return messages

    def render(self):
        return "\n".join(self.aslist())


def nmea0183_telemetry_demo():
    """
    Demonstrate submitting telemetry data in NMEA-0183 sentence format
    over UDP broadcast to `openplotter.local:10110`.

    Synopsis::

        python -m calypso_anemometer.telemetry.nmea0183
    """

    # Setup logging.
    from calypso_anemometer.util import setup_logging

    setup_logging(level=logging.DEBUG)

    # Define example reading.
    reading = CalypsoReading(
        wind_speed=5.69,
        wind_direction=206,
        battery_level=90,
        temperature=33,
        roll=30,
        pitch=-60,
        compass=235,
    )

    # Submit telemetry message to OpenCPN.
    telemetry = NetworkTelemetry(
        host="openplotter.local", port=10110, protocol=NetworkProtocol.UDP, mode=NetworkProtocolMode.BROADCAST
    )
    msg = Nmea0183Messages()
    msg.set_reading(reading)
    telemetry.send(msg.render())


if __name__ == "__main__":
    nmea0183_telemetry_demo()
