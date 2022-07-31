# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import os
import sys
import typing as t

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import CalypsoError
from calypso_anemometer.model import CalypsoDeviceDataRate, CalypsoReading
from calypso_anemometer.telemetry.adapter import TelemetryAdapter
from calypso_anemometer.util import wait_forever

logger = logging.getLogger(__name__)


async def run_engine(workhorse, handler: t.Callable):
    """
    Create a workhorse engine and connect it with the asynchronous handler function for processing readings.
    """
    try:
        worker = workhorse(ble_address=os.getenv("CALYPSO_ADDRESS"))
        async with worker as calypso:
            await handler(calypso)
    except CalypsoError as ex:
        logger.error(ex)
        sys.exit(1)
    return worker


async def handler_factory(
    subscribe: bool = False, target: t.Optional[str] = None, rate: t.Optional[CalypsoDeviceDataRate] = None
) -> t.Callable:
    """
    Create an asynchronous handler function for processing readings.

    :param subscribe: Whether to run in one-shot or continuous mode.
    :param target: Where to submit telemetry data to, and how.
    :param rate: At which rate to sample the readings.

    :return: An asynchronous handler function accepting a reference to a workhorse instance.
    """

    # Optionally enabled telemetry.
    telemetry = None
    if target is not None:
        telemetry = TelemetryAdapter(uri=target)

    # When a reading is received, display it on STDOUT and submit to telemetry adapter.
    def process_reading(reading: CalypsoReading):
        reading.print()
        if telemetry is not None:
            telemetry.submit(reading)

    # Main handler, which receives readings.
    async def handler(calypso: CalypsoDeviceApi):

        # One-shot reading.
        if not subscribe:
            reading = await calypso.get_reading()
            process_reading(reading)

        # Continuous readings.
        else:
            if rate is not None:
                logger.info(f"Setting device data rate to {rate}")
                await calypso.set_datarate(rate)

            await calypso.subscribe_reading(process_reading)
            await wait_forever()

    return handler
