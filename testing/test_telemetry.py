# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import json
import re
from copy import deepcopy

import pytest

from calypso_anemometer.telemetry.adapter import TelemetryAdapter
from calypso_anemometer.telemetry.nmea0183 import Nmea0183Envelope, Nmea0183MessageVWR
from calypso_anemometer.telemetry.signalk import SignalKDeltaMessage
from testing.data import dummy_reading


def test_telemetry_signalk_message():
    bucket = SignalKDeltaMessage(source="Calypso UP10", location="Mast")
    bucket.set_reading(dummy_reading)
    assert bucket.asdict() == {
        "updates": [
            {
                "$source": "calypso-up10",
                "values": [
                    {"path": "environment.outside.temperature", "value": 306.15},
                    {"path": "environment.wind.angleApparent", "value": 3.5953782591083185},
                    {"path": "environment.wind.speedApparent", "value": 5.69},
                    {"path": "navigation.attitude.roll", "value": 0.5235987755982988},
                    {"path": "navigation.attitude.pitch", "value": -1.0471975511965976},
                    {"path": "navigation.attitude.yaw", "value": 4.101523742186674},
                    {"path": "navigation.headingMagnetic", "value": 4.101523742186674},
                    {"path": "electrical.batteries.99.name", "value": "Calypso UP10"},
                    {"path": "electrical.batteries.99.location", "value": "Mast"},
                    {"path": "electrical.batteries.99.capacity.stateOfCharge", "value": 0.9},
                ],
            }
        ]
    }
    assert "updates" in json.loads(bucket.render())


def test_telemetry_nmea0183_wind_into():
    bucket = Nmea0183Envelope()
    reading = deepcopy(dummy_reading)
    reading.wind_direction = 0
    bucket.set_reading(reading)
    assert "$MLVWR,0.0,,11.06,N,5.69,M,20.48,K*28" in bucket.render()


def test_telemetry_nmea0183_wind_downwind():
    bucket = Nmea0183Envelope()
    reading = deepcopy(dummy_reading)
    reading.wind_direction = 180
    bucket.set_reading(reading)
    assert "$MLVWR,180.0,,11.06,N,5.69,M,20.48,K*21" in bucket.render()


def test_telemetry_nmea0183_wind_left_of_bow():
    bucket = Nmea0183Envelope()
    reading = deepcopy(dummy_reading)
    reading.wind_direction = 206
    bucket.set_reading(reading)
    assert "$MLVWR,154.0,L,11.06,N,5.69,M,20.48,K*64" in bucket.render()


def test_telemetry_nmea0183_wind_right_of_bow():
    bucket = Nmea0183Envelope()
    reading = deepcopy(dummy_reading)
    reading.wind_direction = 42
    bucket.set_reading(reading)
    assert "$MLVWR,42.0,R,11.06,N,5.69,M,20.48,K*4C" in bucket.render()


def test_telemetry_nmea0183_wind_zero():
    bucket = Nmea0183Envelope()
    reading = deepcopy(dummy_reading)
    reading.wind_speed = 0
    bucket.set_reading(reading)
    assert "$MLVWR,0.0,,0.0,N,0.0,M,0.0,K*1A" in bucket.render()


def test_telemetry_nmea0183_compass_heading():
    bucket = Nmea0183Envelope()
    reading = deepcopy(dummy_reading)
    reading.wind_speed = 0
    bucket.set_reading(reading)
    assert "$MLHDT,235.0,T*27" in bucket.render()


def test_nmea0183message_vwr_float_value():
    assert Nmea0183MessageVWR.float_value(42.42) == 42.42
    assert Nmea0183MessageVWR.float_value(None) == ""


def test_nmea0183message_vwr_render_success():
    bucket = Nmea0183MessageVWR(direction_degrees=42.42, speed_meters_per_second=5.42)
    assert "$MLVWR,42.42,R,10.54,N,5.42,M,19.51,K*77" in bucket.to_message().render()


def test_telemetry_adapter_signalk_success():
    telemetry = TelemetryAdapter(uri="udp+signalk+delta://localhost:64123")
    bucket = telemetry.submit(dummy_reading)
    assert isinstance(bucket, SignalKDeltaMessage)


def test_telemetry_adapter_nmea0183_success():
    telemetry = TelemetryAdapter(uri="udp+broadcast+nmea0183://255.255.255.255:60110")
    bucket = telemetry.submit(dummy_reading)
    assert isinstance(bucket, Nmea0183Envelope)


def test_telemetry_adapter_unknown_failure():
    with pytest.raises(KeyError) as ex:
        telemetry = TelemetryAdapter(uri="foobar://localhost:12345")
        telemetry.submit(dummy_reading)
    assert ex.match(re.escape("NetworkProtocol for URI 'foobar://localhost:12345' not supported"))


def test_telemetry_adapter_handler_failure():
    with pytest.raises(KeyError) as ex:
        telemetry = TelemetryAdapter(uri="udp+broadcast+nmea0183://255.255.255.255:60110")
        telemetry.handler = None
        telemetry.submit(dummy_reading)
    assert ex.match("No telemetry handler established")
