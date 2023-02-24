# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import sys

import pytest

if sys.version_info < (3, 8, 0):
    raise pytest.skip(reason="AsyncMock not supported on Python 3.7", allow_module_level=True)
from unittest.mock import AsyncMock, call

from pytest_mock import MockerFixture

import calypso_anemometer
from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.model import CalypsoDeviceCompassStatus, CalypsoDeviceDataRate


@pytest.mark.asyncio
async def test_set_datarate_success(mocker: MockerFixture, caplog):
    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.write_gatt_char", AsyncMock(return_value=None))

    spy = mocker.spy(calypso_anemometer.core.BleakClient, "write_gatt_char")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        await calypso.set_datarate(CalypsoDeviceDataRate.HZ_8)

    assert spy.mock_calls == [call("0000a002-0000-1000-8000-00805f9b34fb", data=b"\x08", response=True)]

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Setting data rate to 8" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_set_compass_enabled(mocker: MockerFixture, caplog):
    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.write_gatt_char", AsyncMock(return_value=None))

    spy = mocker.spy(calypso_anemometer.core.BleakClient, "write_gatt_char")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        await calypso.set_compass(CalypsoDeviceCompassStatus.ON)

    assert spy.mock_calls == [call("0000a003-0000-1000-8000-00805f9b34fb", data=b"\x01", response=True)]

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Setting compass status to 1" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_set_compass_disabled(mocker: MockerFixture, caplog):
    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.write_gatt_char", AsyncMock(return_value=None))

    spy = mocker.spy(calypso_anemometer.core.BleakClient, "write_gatt_char")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        await calypso.set_compass(CalypsoDeviceCompassStatus.OFF)

    assert spy.mock_calls == [call("0000a003-0000-1000-8000-00805f9b34fb", data=b"\x00", response=True)]

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Setting compass status to 0" in caplog.messages
    assert "Disconnecting" in caplog.messages
