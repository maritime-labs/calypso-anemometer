# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import asyncio
import concurrent
import sys

import pytest

if sys.version_info < (3, 8, 0):
    raise pytest.skip(reason="AsyncMock not supported on Python 3.7", allow_module_level=True)
from unittest.mock import AsyncMock, call

from bleak import BleakError
from bleak.backends.device import BLEDevice
from pytest_mock import MockerFixture

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import BluetoothAdapterError, BluetoothConversationError, BluetoothTimeoutError


@pytest.mark.asyncio
async def test_connect_contextmanager_success(mocker: MockerFixture, caplog):

    mocker.patch(
        "calypso_anemometer.core.BleakScanner.find_device_by_filter",
        AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
    )
    client = mocker.patch("calypso_anemometer.core.BleakClient", autospec=True)

    async with CalypsoDeviceApi() as calypso:
        assert calypso.ble_address == "bar"

    assert client.mock_calls == [
        call("bar", timeout=10.0, adapter="hci0"),
        call().connect(),
        call().disconnect(),
    ]
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Found device at address: bar: foo" in caplog.messages
    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_connect_adapter_off_failure(mocker: MockerFixture, caplog):

    mocker.patch(
        "calypso_anemometer.core.BleakClient.connect",
        AsyncMock(side_effect=BleakError("Bluetooth device is turned off")),
    )

    calypso = CalypsoDeviceApi(ble_address="bar")
    with pytest.raises(BluetoothAdapterError) as ex:
        await calypso.connect()

    assert ex.match("Bluetooth device is turned off")

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Conversation went south: BleakError: Bluetooth device is turned off" in caplog.messages


@pytest.mark.asyncio
async def test_connect_any_error_failure(mocker: MockerFixture, caplog):

    mocker.patch(
        "calypso_anemometer.core.BleakClient.connect", AsyncMock(side_effect=BleakError("Something went wrong"))
    )

    calypso = CalypsoDeviceApi(ble_address="bar")
    with pytest.raises(BluetoothConversationError) as ex:
        await calypso.connect()

    assert ex.match("Something went wrong")

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Conversation went south: BleakError: Something went wrong" in caplog.messages


@pytest.mark.asyncio
async def test_connect_asyncio_timeout_failure(mocker: MockerFixture, caplog):

    mocker.patch(
        "calypso_anemometer.core.BleakClient.connect",
        AsyncMock(side_effect=asyncio.TimeoutError("Device did not respond in time")),
    )

    calypso = CalypsoDeviceApi(ble_address="bar")
    with pytest.raises(BluetoothTimeoutError) as ex:
        await calypso.connect()

    assert ex.match("Device did not respond in time")

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "TimeoutError: Device did not respond in time" in caplog.messages


@pytest.mark.asyncio
async def test_connect_futures_timeout_failure(mocker: MockerFixture, caplog):

    mocker.patch(
        "calypso_anemometer.core.BleakClient.connect",
        AsyncMock(side_effect=concurrent.futures.TimeoutError("Device did not respond in time")),
    )

    calypso = CalypsoDeviceApi(ble_address="bar")
    with pytest.raises(BluetoothTimeoutError) as ex:
        await calypso.connect()

    assert ex.match("Device did not respond in time")

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "TimeoutError: Device did not respond in time" in caplog.messages


@pytest.mark.asyncio
async def test_connect_disconnect_failure(mocker: MockerFixture, caplog):

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch(
        "calypso_anemometer.core.BleakClient.disconnect", AsyncMock(side_effect=BleakError("Error on disconnect"))
    )

    calypso = CalypsoDeviceApi(ble_address="bar")
    await calypso.connect()
    await calypso.disconnect()

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Disconnecting" in caplog.messages
    assert "Disconnect failed" in caplog.messages
