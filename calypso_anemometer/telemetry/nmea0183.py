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

-- http://www.nmea.de/nmea0183datensaetze.html#vwr


CLI sender / receiver
=====================

Submit and receive NMEA-0183 over UDP broadcast on the command line.
See https://github.com/maritime-labs/calypso-anemometer/blob/main/doc/preflight.rst#nmea-0183-telemetry-over-udp

"""
import dataclasses
import logging
import struct
import typing as t
from binascii import hexlify

from calypso_anemometer.model import CalypsoReading

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
        checksum = self.checksum_hexlified(message)
        message += f"*{checksum}"
        return message

    @classmethod
    def checksum(cls, message) -> int:
        """
        Calculating the checksum is very easy. It is the representation of two hexadecimal characters of
        an XOR of all characters in the sentence between – but not including – the $ and the * character.

        https://rietman.wordpress.com/2008/09/25/how-to-calculate-the-nmea-checksum/
        """
        checksum: int = 0
        for char in message[1:]:
            checksum ^= ord(char)
        return checksum

    @classmethod
    def checksum_hexlified(cls, message) -> str:
        checksum = cls.checksum(message)
        return hexlify(struct.pack("B", checksum)).decode().upper()


class Nmea0183MessageBase:
    @staticmethod
    def float_value(value, default=""):
        if value is None:
            value = default
        else:
            value = float(value)
        return value


@dataclasses.dataclass
class Nmea0183MessageHDT(Nmea0183MessageBase):
    """
    Represent and serialize NMEA-0183 HDT message.

    HDT - Heading - True

    Actual vessel heading in degrees Ture produced by any
    device or system producing true heading.

            1   2 3
            |   | |
     $--HDT,x.x,T*hh<CR><LF>

     Field Number:
      1) Heading Degrees, true
      2) T = True
      3) Checksum

    References:
    - http://aprs.gids.nl/nmea/#hdt
    - https://github.com/maritime-labs/calypso-anemometer/issues/12
    """

    IDENTIFIER = "$MLHDT"
    heading_degrees: float

    def to_message(self):
        """
        Factory for generic `Nmea0183Message`.
        """
        return Nmea0183GenericMessage(
            identifier=self.IDENTIFIER,
            fields=[
                self.float_value(self.heading_degrees),
                "T",
            ],
        )


@dataclasses.dataclass
class Nmea0183MessageVWR(Nmea0183MessageBase):
    """
    Represent and serialize NMEA-0183 VWR message.

    VWR - Relative Wind Speed and Angle
    """

    IDENTIFIER = "$MLVWR"
    direction_degrees: float
    speed_meters_per_second: float

    @property
    def direction_magnitude_in_degrees(self) -> float:
        return abs(self.wind_direction_180)

    @property
    def wind_direction_180(self) -> int:
        angle = self.direction_degrees
        return (angle > 180) and angle - 360 or angle

    @property
    def direction_left_right_of_bow(self) -> str:
        if -180 < self.wind_direction_180 < 0:
            indicator = "L"
        elif 0 < self.wind_direction_180 < 180:
            indicator = "R"
        else:
            indicator = ""
        return indicator

    @property
    def speed_knots(self) -> float:
        return round(self.speed_meters_per_second * 1.943844, 2)

    @property
    def speed_kilometers_per_hour(self) -> float:
        return round(self.speed_meters_per_second * 3.6, 2)

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
                self.float_value(self.direction_magnitude_in_degrees),
                self.direction_left_right_of_bow,
                self.float_value(self.speed_knots),
                "N",
                self.float_value(self.speed_meters_per_second),
                "M",
                self.float_value(self.speed_kilometers_per_hour),
                "K",
            ],
        )


@dataclasses.dataclass
class Nmea0183MessageXDRGeneric(Nmea0183MessageBase):
    """
    Represent and serialize NMEA-0183 XDR message.

    XDR - Transducer Measurements

    Different kinds of values like temperature, pressure, and angle.

    Here, it will be used to emit air temperature and battery level data:

    # Air temperature
    $MLXDR,C,42.42,C,AIRTEMP#CAL

    # Battery level
    $MLXDR,L,0.9,R,BATT#CAL

                1 2   3 4       n
    |   |   |   |       |
    *  $--XDR,a,x.x,a,c--c, ..... *hh<CR><LF>

    Field Number:
    1) Transducer Type
    2) Measurement Data
    3) Units of measurement
    4) Name of transducer
    x) More of the same
    n) Checksum

    Examples:
    $IIXDR,C,19.52,C,TempAir*19
    $IIXDR,P,1.02481,B,Barometer*29

    References:
    - https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:advanced_features:nmea_sentences#xdr
    - https://github.com/maritime-labs/calypso-anemometer/issues/21
    """

    IDENTIFIER = "$MLXDR"
    transducer_type: str
    value: float
    measurement_unit: str
    name: str

    def to_message(self):
        """
        Factory for generic `Nmea0183Message`.
        """
        return Nmea0183GenericMessage(
            identifier=self.IDENTIFIER,
            fields=[
                self.transducer_type,
                self.float_value(self.value),
                self.measurement_unit,
                self.name,
            ],
        )


@dataclasses.dataclass
class Nmea0183MessageXDRPitchRoll(Nmea0183MessageBase):
    """
    Represent and serialize NMEA-0183 XDR message.

    XDR - Transducer Measurements

    Different kinds of values like temperature, pressure, and angle.

    Here, it will be used to emit compass/gyro pitch and roll data:
    $MLXDR,A,-42.42,D,PTCH#CAL,A,30.07,D,ROLL#CAL

                1 2   3 4       n
    |   |   |   |       |
    *  $--XDR,a,x.x,a,c--c, ..... *hh<CR><LF>

    Field Number:
    1) Transducer Type
    2) Measurement Data
    3) Units of measurement
    4) Name of transducer
    x) More of the same
    n) Checksum

    Examples:
    $IIXDR,C,19.52,C,TempAir*19
    $IIXDR,P,1.02481,B,Barometer*29

    References:
    - https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn:opencpn_user_manual:advanced_features:nmea_sentences#xdr
    - https://github.com/maritime-labs/calypso-anemometer/issues/12
    """

    IDENTIFIER = "$MLXDR"
    pitch_degrees: float
    roll_degrees: float

    def to_message(self):
        """
        Factory for generic `Nmea0183Message`.
        """
        return Nmea0183GenericMessage(
            identifier=self.IDENTIFIER,
            fields=[
                # Pitch
                "A",
                self.float_value(self.pitch_degrees),
                "D",
                "PTCH#CAL",
                # Roll
                "A",
                self.float_value(self.roll_degrees),
                "D",
                "ROLL#CAL",
            ],
        )


@dataclasses.dataclass
class Nmea0183Envelope:
    """
    Represent and render a list of NMEA-0183 messages.
    """

    items: t.Optional[t.List[Nmea0183GenericMessage]] = None

    def set_reading(self, reading: CalypsoReading):
        """
        Derive NMEA-0183 VWR message from measurement reading.
        """
        reading = reading.adjusted()
        hdt = Nmea0183MessageHDT(
            heading_degrees=reading.heading,
        )
        vwr = Nmea0183MessageVWR(
            direction_degrees=reading.wind_direction,
            speed_meters_per_second=reading.wind_speed,
        )
        xdr_air_temperature = Nmea0183MessageXDRGeneric(
            transducer_type="C",
            value=reading.temperature,
            measurement_unit="C",
            name="AIRTEMP#CAL",
        )
        xdr_battery_level = Nmea0183MessageXDRGeneric(
            transducer_type="L",
            value=round(reading.battery_level / 100, 2),
            measurement_unit="R",
            name="BATT#CAL",
        )
        xdr_pitch_roll = Nmea0183MessageXDRPitchRoll(
            pitch_degrees=reading.pitch,
            roll_degrees=reading.roll,
        )
        self.items = [
            hdt.to_message(),
            vwr.to_message(),
            xdr_pitch_roll.to_message(),
            xdr_air_temperature.to_message(),
            xdr_battery_level.to_message(),
        ]

    def aslist(self):
        """
        Render measurement items to multiple NMEA-0183 sentences.
        """
        messages = [item.render() for item in self.items]
        return messages

    def render(self):
        return "\r\n".join(self.aslist())
