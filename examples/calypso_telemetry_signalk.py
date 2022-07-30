# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging

from calypso_anemometer.model import CalypsoReading
from calypso_anemometer.telemetry import NetworkTelemetry, SignalKDeltaMessage
from calypso_anemometer.telemetry.model import NetworkProtocol

logger = logging.getLogger(__name__)


def calypso_signalk_telemetry_demo(host="localhost", port=4123):
    """
    Demonstrate submitting telemetry data in SignalK Delta Format
    over UDP to SignalK server `openplotter.local:4123`.

    Synopsis::

        python examples/calypso_telemetry_signalk.py
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

    # Submit telemetry message to SignalK.
    telemetry = NetworkTelemetry(host=host, port=port, protocol=NetworkProtocol.UDP)
    msg = SignalKDeltaMessage(source="Calypso UP10", location="Mast")
    msg.set_reading(reading)
    telemetry.send(msg.render())


if __name__ == "__main__":  # pragma: nocover
    calypso_signalk_telemetry_demo(host="localhost", port=4123)
