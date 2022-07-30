# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from copy import deepcopy

from calypso_anemometer.model import (
    CalypsoDeviceCompassStatus,
    CalypsoDeviceDataRate,
    CalypsoDeviceInfo,
    CalypsoDeviceMode,
    CalypsoDeviceStatus,
)
from testing.conf import test_reading


def test_calypso_reading_vanilla():
    reading = deepcopy(test_reading)
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
    reading = deepcopy(test_reading)
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
    device_status = CalypsoDeviceStatus(
        mode=CalypsoDeviceMode.NORMAL,
        rate=CalypsoDeviceDataRate.HZ_8,
        compass=CalypsoDeviceCompassStatus.ON,
    )
    assert device_status.aslabeldict() == {"compass": "ON", "mode": "NORMAL", "rate": "HZ_8"}
