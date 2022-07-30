# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import json
import re
from copy import deepcopy

import pytest

from calypso_anemometer.telemetry import Nmea0183Messages, SignalKDeltaMessage, TelemetryAdapter
from calypso_anemometer.telemetry.nmea0183 import Nmea0183MessageIIVWR
from testing.conf import test_reading


def test_telemetry_signalk_message():
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
    assert msg.render() == "$IIVWR,0.0,,11.06,N,5.69,M,20.48,K*29"


def test_telemetry_nmea0183_wind_downwind():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_direction = 180
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,180.0,,11.06,N,5.69,M,20.48,K*20"


def test_telemetry_nmea0183_wind_left_of_bow():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_direction = 206
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,154.0,L,11.06,N,5.69,M,20.48,K*65"


def test_telemetry_nmea0183_wind_right_of_bow():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_direction = 42
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,42.0,R,11.06,N,5.69,M,20.48,K*4D"


def test_telemetry_nmea0183_wind_zero():
    msg = Nmea0183Messages()
    reading = deepcopy(test_reading)
    reading.wind_speed = 0
    msg.set_reading(reading)
    assert msg.render() == "$IIVWR,0.0,,0.0,N,0.0,M,0.0,K*1B"


def test_nmea0183messageiivwr_convert_value():
    assert Nmea0183MessageIIVWR.convert_value(42.42) == 42.42
    assert Nmea0183MessageIIVWR.convert_value(None) == ""


def test_nmea0183messageiivwr_render_success():
    msg = Nmea0183MessageIIVWR(direction_degrees=42.42, speed_meters_per_second=5.42)
    assert msg.to_message().render() == "$IIVWR,42.42,R,10.54,N,5.42,M,19.51,K*76"


def test_telemetry_adapter_signalk_success():
    telemetry = TelemetryAdapter(uri="udp+signalk+delta://localhost:4123")
    msg = telemetry.submit(test_reading)
    assert isinstance(msg, SignalKDeltaMessage)


def test_telemetry_adapter_nmea0183_success():
    telemetry = TelemetryAdapter(uri="udp+broadcast+nmea0183://255.255.255.255:10110")
    msg = telemetry.submit(test_reading)
    assert isinstance(msg, Nmea0183Messages)


def test_telemetry_adapter_unknown_failure():
    with pytest.raises(KeyError) as ex:
        telemetry = TelemetryAdapter(uri="foobar://localhost:12345")
        telemetry.submit(test_reading)
    assert ex.match(re.escape("NetworkProtocol for URI 'foobar://localhost:12345' not supported"))


def test_telemetry_adapter_handler_failure():
    with pytest.raises(KeyError) as ex:
        telemetry = TelemetryAdapter(uri="udp+broadcast+nmea0183://255.255.255.255:10110")
        telemetry.handler = None
        telemetry.submit(test_reading)
    assert ex.match("No telemetry handler established")
