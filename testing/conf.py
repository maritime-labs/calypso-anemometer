# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3


# Define example reading.
from calypso_anemometer.model import CalypsoReading

test_reading = CalypsoReading(
    wind_speed=5.69,
    wind_direction=206,
    battery_level=90,
    temperature=33,
    roll=30,
    pitch=-60,
    compass=235,
)
