# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from copy import deepcopy

from calypso_anemometer.model import CalypsoDeviceInfo, CalypsoReading
from testing.data import dummy_device_status, dummy_reading, dummy_wire_message_good


def test_decode_wiredata():
    """
    Ex.
    0-1.  hex2dec(00 00) => 0 / 100 => 0
    2-3.  hex2dec(01 3F) => 319 (degrees)
    4.    hex2dec(04) => 4 * 10 => 40%
    5.    hex2dec(7C) => 124 - 100 => 24 (degrees C)
    6.    hex2dec(00) => 0 - 90 => -90 (degrees)
    7.    hex2dec(00) => 0 - 90 => -90 (degrees)
    8-9.  360 - hex2dec(00 00) => 360 - 0 => 360
    """
    buffer = dummy_wire_message_good
    data = CalypsoReading.from_buffer(buffer)
    assert data == CalypsoReading(
        wind_speed=5.69, wind_direction=206, battery_level=90, temperature=33, roll=30, pitch=-60, compass=235
    )


def test_calypso_reading_vanilla():
    reading = deepcopy(dummy_reading)
    assert reading.asdict() == dict(
        wind_speed=5.69,
        wind_direction=206,
        battery_level=90,
        temperature=33,
        roll=30,
        pitch=-60,
        compass=235,
    )


def test_calypso_reading_adjusted():
    """
    Proof that compensation for sticky wind direction works as expected.

    I.e., synthesize zeroing of wind direction, when wind speed goes zero.
    """
    reading = deepcopy(dummy_reading)
    reading.wind_speed = 0.0
    assert reading.adjusted().asdict() == dict(
        wind_speed=0.0,
        wind_direction=0,
        battery_level=90,
        temperature=33,
        roll=30,
        pitch=-60,
        compass=235,
    )


def test_device_info():
    device_info = CalypsoDeviceInfo(
        ble_address="foo",
        manufacturer_name="bar",
        model_number="baz",
        serial_number="qux",
    )
    assert device_info.asdict() == {
        "ble_address": "foo",
        "manufacturer_name": "bar",
        "model_number": "baz",
        "serial_number": "qux",
        "hardware_revision": None,
        "firmware_revision": None,
        "software_revision": None,
    }


def test_device_status():
    assert dummy_device_status.aslabeldict() == {"compass": "ON", "mode": "NORMAL", "rate": "HZ_8"}
