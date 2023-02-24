# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from unittest.mock import Mock

import pytest

from calypso_anemometer.fake import MAXIMUM_VALUES, MINIMUM_VALUES, CalypsoDeviceApiFake
from calypso_anemometer.model import CalypsoDeviceDataRate, CalypsoReading


@pytest.mark.asyncio
async def test_discover():
    fake = CalypsoDeviceApiFake()
    assert await fake.discover() is True


@pytest.mark.asyncio
async def test_set_datarate():
    fake = CalypsoDeviceApiFake()
    await fake.set_datarate(CalypsoDeviceDataRate.HZ_8)
    assert fake.datarate == CalypsoDeviceDataRate.HZ_8


@pytest.mark.asyncio
async def test_subscribe_once():
    callback_mock = Mock()
    async with CalypsoDeviceApiFake() as fake:
        await fake.set_datarate(CalypsoDeviceDataRate.HZ_8)
        await fake.subscribe_reading(callback=callback_mock, run_once=True)

    callback_mock.assert_called_once_with(
        CalypsoReading(wind_speed=1, wind_direction=1, battery_level=1, temperature=-99, roll=-89, pitch=-89, heading=1)
    )


@pytest.mark.asyncio
async def test_reading_wrap_around():
    fake = CalypsoDeviceApiFake()
    fake.reading = MAXIMUM_VALUES
    reading = await fake.produce_fake_reading()
    assert reading == MINIMUM_VALUES
