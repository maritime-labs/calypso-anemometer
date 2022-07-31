# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from calypso_anemometer.model import (
    CalypsoDeviceCompassStatus,
    CalypsoDeviceDataRate,
    CalypsoDeviceInfo,
    CalypsoDeviceMode,
    CalypsoDeviceStatus,
    CalypsoReading,
)

# Define example reading.
dummy_reading = CalypsoReading(
    wind_speed=5.69,
    wind_direction=206,
    battery_level=90,
    temperature=33,
    roll=30,
    pitch=-60,
    compass=235,
)

# Define example wire messages.
dummy_wire_message_good = b"\x39\x02\xce\x00\x09\x85\x78\x1e\x7d\x00"
dummy_wire_message_bad = b"\xaa"

# Define example device info and status objects.
dummy_device_info = CalypsoDeviceInfo(
    ble_address="bar",
    manufacturer_name="acme",
    model_number="baz",
    serial_number="qux",
)
dummy_device_status = CalypsoDeviceStatus(
    mode=CalypsoDeviceMode.NORMAL,
    rate=CalypsoDeviceDataRate.HZ_8,
    compass=CalypsoDeviceCompassStatus.ON,
)
