# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import asyncio

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.model import CalypsoReading
from calypso_anemometer.util import wait_forever


async def calypso_subscribe_demo():
    def process_reading(reading: CalypsoReading):
        reading.dump()

    async with CalypsoDeviceApi() as calypso:
        await calypso.subscribe_reading(process_reading)
        await wait_forever()


if __name__ == "__main__":  # pragma: nocover
    asyncio.run(calypso_subscribe_demo())
