# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from calypso_anemometer.model import CalypsoReading


def test_decode():
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
    buffer = b"\x39\x02\xce\x00\x09\x85\x78\x1e\x7d\x00"
    data = CalypsoReading.from_buffer(buffer)
    assert data == CalypsoReading(
        wind_speed=5.69, wind_direction=206, battery_level=90, temperature=33, roll=30, pitch=-60, compass=235
    )
