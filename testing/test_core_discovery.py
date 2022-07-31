# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from unittest import mock

import pytest
from bleak import BleakError
from bleak.backends.device import BLEDevice

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import BluetoothAdapterError, BluetoothDiscoveryError


@pytest.mark.asyncio
async def test_discover_vanilla_unneeded_success(caplog):
    calypso = CalypsoDeviceApi(ble_address="foobar")
    assert await calypso.discover() is True


@pytest.mark.asyncio
@mock.patch("calypso_anemometer.core.BleakScanner", autospec=True)
async def test_discover_vanilla_found_success(scanner, caplog):

    scanner.find_device_by_filter.return_value = BLEDevice(name="foo", address="bar")

    calypso = CalypsoDeviceApi()
    assert await calypso.discover() is True
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Found device at address: bar: foo" in caplog.messages


@pytest.mark.asyncio
@mock.patch("calypso_anemometer.core.BleakScanner", autospec=True)
async def test_discover_vanilla_notfound_success(scanner, caplog):
    scanner.find_device_by_filter.return_value = None

    calypso = CalypsoDeviceApi()
    assert await calypso.discover() is False
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Unable to find device" in caplog.messages


@pytest.mark.asyncio
@mock.patch("calypso_anemometer.core.BleakClient", autospec=True)
@mock.patch("calypso_anemometer.core.BleakScanner", autospec=True)
async def test_discover_contextmanager_found_success(scanner, client, caplog):
    scanner.find_device_by_filter.return_value = BLEDevice(name="foo", address="bar")

    async with CalypsoDeviceApi() as calypso:
        assert calypso.ble_address == "bar"
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Found device at address: bar: foo" in caplog.messages


@pytest.mark.asyncio
@mock.patch("calypso_anemometer.core.BleakClient", autospec=True)
@mock.patch("calypso_anemometer.core.BleakScanner", autospec=True)
async def test_discover_contextmanager_notfound_success(scanner, client, caplog):
    scanner.find_device_by_filter.return_value = None

    with pytest.raises(BluetoothDiscoveryError) as ex:
        async with CalypsoDeviceApi():
            pass
    assert ex.match("Unable to discover device Calypso UP10 anemometer")
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Unable to find device" in caplog.messages


@pytest.mark.asyncio
@mock.patch("calypso_anemometer.core.BleakScanner", autospec=True)
async def test_discover_adapter_off_failure(scanner, caplog):
    scanner.find_device_by_filter.side_effect = BleakError("Bluetooth device is turned off")

    calypso = CalypsoDeviceApi()
    with pytest.raises(BluetoothAdapterError) as ex:
        assert await calypso.discover() is False
    assert ex.match("Bluetooth device is turned off")
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages


@pytest.mark.asyncio
@mock.patch("calypso_anemometer.core.BleakScanner", autospec=True)
async def test_discover_any_error_failure(scanner, caplog):
    scanner.find_device_by_filter.side_effect = BleakError("Something went wrong")

    calypso = CalypsoDeviceApi()
    with pytest.raises(BleakError) as ex:
        assert await calypso.discover() is False
    assert ex.match("Something went wrong")
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
