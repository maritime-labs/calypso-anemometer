# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging

from calypso_anemometer.model import CalypsoReading
from calypso_anemometer.telemetry.model import NetworkProtocol, NetworkProtocolMode
from calypso_anemometer.telemetry.network import NetworkTelemetry
from calypso_anemometer.telemetry.nmea0183 import Nmea0183Envelope

logger = logging.getLogger(__name__)


def calypso_nmea0183_telemetry_demo(host="255.255.255.255", port=10110):
    """
    Demonstrate submitting telemetry data in NMEA-0183 sentence format
    over UDP broadcast to `255.255.255.255:10110`.

    Synopsis::

        python examples/calypso_telemetry_nmea0183.py
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

    # Broadcast telemetry message, e.g. to OpenCPN.
    telemetry = NetworkTelemetry(host=host, port=port, protocol=NetworkProtocol.UDP, mode=NetworkProtocolMode.BROADCAST)
    bucket = Nmea0183Envelope()
    bucket.set_reading(reading)
    telemetry.send(bucket.render())


if __name__ == "__main__":  # pragma: nocover
    calypso_nmea0183_telemetry_demo(host="255.255.255.255", port=10110)
