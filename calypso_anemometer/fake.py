# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses
import logging
from copy import deepcopy
from typing import Callable, Optional

import aiorate

from calypso_anemometer.model import CalypsoDeviceDataRate, CalypsoReading, Settings

logger = logging.getLogger(__name__)

MINIMUM_VALUES = CalypsoReading(
    wind_speed=0,
    wind_direction=0,
    battery_level=0,
    temperature=-100,
    roll=-90,
    pitch=-90,
    compass=0,
)

MAXIMUM_VALUES = CalypsoReading(
    wind_speed=40,
    wind_direction=360,
    battery_level=100,
    temperature=+100,
    roll=+90,
    pitch=+90,
    compass=360,
)


class CalypsoDeviceApiFake:

    NAME = "calypso-up10-fake"
    DESCRIPTION = "Calypso UP10 anemometer fake device"

    def __init__(self, settings: Optional[Settings] = None, ble_address: Optional[str] = None):
        if settings is None:
            settings = Settings(ble_address=ble_address)
        self.settings = settings
        self.ble_address = settings.ble_address
        self.datarate: CalypsoDeviceDataRate = CalypsoDeviceDataRate.HZ_4
        self.reading: Optional[CalypsoReading] = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
        if exc_val is not None:  # pragma: no cover
            raise exc_val

    async def discover(self, force=False) -> bool:
        self.ble_address = "fake-ble-address"
        return True

    async def connect(self):
        self.reading = deepcopy(MINIMUM_VALUES)

    async def disconnect(self):
        self.reading = None

    async def set_datarate(self, rate: CalypsoDeviceDataRate):
        self.datarate = rate

    async def get_reading(self):
        logger.info("Producing reading")
        return await self.produce_fake_reading()

    async def subscribe_reading(self, callback: Optional[Callable] = None, run_once: Optional[bool] = False):
        """
        Fake async reading producer task, emulating responses to a BLE subscribe/notify.
        """
        logger.info("Subscribing to readings")
        rate = aiorate.Rate(float(self.datarate.value))
        while True:
            reading = await self.produce_fake_reading()
            if callback is not None:
                callback(reading)
            await rate.sleep()
            if run_once:
                break

    async def produce_fake_reading(self):
        """
        Produce an artificial reading with incrementing values,
        wrapping around at a maximum limit per measurement.
        """
        for field in dataclasses.fields(self.reading):
            current_value = getattr(self.reading, field.name)
            minimum_value = getattr(MINIMUM_VALUES, field.name)
            maximum_value = getattr(MAXIMUM_VALUES, field.name)
            current_value += 1
            if current_value > maximum_value:
                current_value = minimum_value
            setattr(self.reading, field.name, current_value)
        return self.reading
