# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import json
from copy import deepcopy

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


def test_telemetry_nmea0183_wind_into():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_direction = 0
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,0.0,,,N,5.69,M,,K"


def test_telemetry_nmea0183_wind_downwind():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_direction = 180
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,180.0,,,N,5.69,M,,K"


def test_telemetry_nmea0183_wind_left_of_bow():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_direction = 206
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,154.0,L,,N,5.69,M,,K"


def test_telemetry_nmea0183_wind_right_of_bow():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_direction = 42
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,42.0,R,,N,5.69,M,,K"
