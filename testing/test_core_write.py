# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from unittest.mock import AsyncMock, call

import pytest
from pytest_mock import MockerFixture

import calypso_anemometer
from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.model import CalypsoDeviceDataRate


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
