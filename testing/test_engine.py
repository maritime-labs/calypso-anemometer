# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import sys

import pytest

from calypso_anemometer.model import Settings

if sys.version_info < (3, 8, 0):
    raise pytest.skip(reason="AsyncMock not supported on Python 3.7", allow_module_level=True)

from unittest.mock import AsyncMock

from bleak.backends.device import BLEDevice
from pytest_mock import MockerFixture

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.engine import handler_factory, run_engine
from testing.data import dummy_wire_message_good


@pytest.mark.asyncio
async def test_run_engine_vanilla_success(mocker: MockerFixture):

    mocker.patch(
        "calypso_anemometer.core.BleakScanner.find_device_by_filter",
        AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
    )
    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))

    handler = await handler_factory()
    worker: CalypsoDeviceApi = await run_engine(workhorse=CalypsoDeviceApi, handler=handler)
    assert worker.ble_address == "bar"


@pytest.mark.asyncio
async def test_run_engine_with_address_success(mocker: MockerFixture):

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))

    settings = Settings(ble_address="F8:C7:2C:EC:13:D0")
    handler = await handler_factory()
    worker: CalypsoDeviceApi = await run_engine(workhorse=CalypsoDeviceApi, settings=settings, handler=handler)
    assert worker.ble_address == "F8:C7:2C:EC:13:D0"
