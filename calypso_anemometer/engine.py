# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import sys
import typing as t

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import CalypsoError
from calypso_anemometer.model import CalypsoDeviceDataRate, CalypsoReading, Settings
from calypso_anemometer.telemetry.adapter import TelemetryAdapter
from calypso_anemometer.util import wait_forever

logger = logging.getLogger(__name__)


async def run_engine(workhorse, handler: t.Callable, settings: t.Optional[Settings] = None):
    """
    Create a workhorse engine and connect it with the asynchronous handler function for processing readings.
    """
    try:
        worker = workhorse(settings=settings)
        async with worker as calypso:
            await handler(calypso)
    except CalypsoError as ex:
        logger.error(ex)
        sys.exit(1)
    return worker


async def handler_factory(
    subscribe: bool = False,
    target: t.Optional[str] = None,
    rate: t.Optional[CalypsoDeviceDataRate] = None,
    quiet: bool = False,
) -> t.Callable:
    """
    Create an asynchronous handler function for processing readings.

    :param subscribe: Whether to run in one-shot or continuous mode.
    :param target: Where to submit telemetry data to, and how.
    :param rate: At which rate to sample the readings.
    :param quiet: Do not print to stdout or stderr.

    :return: An asynchronous handler function accepting a reference to a workhorse instance.
    """

    message_counter = 0
    message_counter_log_each = 25

    # Optionally enable telemetry.
    telemetry = None
    if target is not None:
        telemetry = TelemetryAdapter(uri=target)

    # When a reading is received, optionally display on STDOUT or hand over to telemetry adapter.
    def process_reading(reading: CalypsoReading):
        nonlocal message_counter
        message_counter += 1
        if not quiet:
            reading.print()
        if telemetry is not None:
            telemetry.submit(reading)
        if message_counter % message_counter_log_each == 0:
            logger.info(f"Processed readings: {message_counter}")

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
