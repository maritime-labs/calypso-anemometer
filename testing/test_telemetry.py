# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import json

from calypso_anemometer.telemetry import Nmea0183Messages, SignalKDeltaMessage
from testing.conf import test_reading


def test_telemetry_signalk():
    msg = SignalKDeltaMessage(source="Calypso UP10", location="Mast")
    msg.set_reading(test_reading)
    assert msg.asdict() == {
        "updates": [
            {
                "$source": "calypso-up10",
                "values": [
                    {"path": "environment.outside.temperature", "value": 33},
                    {"path": "environment.wind.angleApparent", "value": 206},
                    {"path": "environment.wind.speedApparent", "value": 5.69},
                    {"path": "navigation.attitude.roll", "value": 30},
                    {"path": "navigation.attitude.pitch", "value": -60},
                    {"path": "navigation.attitude.yaw", "value": 235},
                    {"path": "navigation.headingMagnetic", "value": 235},
                    {"path": "electrical.batteries.99.name", "value": "Calypso UP10"},
                    {"path": "electrical.batteries.99.location", "value": "Mast"},
                    {"path": "electrical.batteries.99.capacity.stateOfCharge", "value": 90},
                ],
            }
        ]
    }
    assert "updates" in json.loads(msg.render())


def test_telemetry_nmea0183():
    msg = Nmea0183Messages()
    msg.set_reading(test_reading)
    assert msg.render() == "$$IIVWR,206.0,,,N,5.69,M,,K\n"
