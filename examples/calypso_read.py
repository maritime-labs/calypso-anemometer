# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import asyncio

from calypso_anemometer.core import CalypsoDeviceApi


async def calypso_read_demo():
    async with CalypsoDeviceApi() as calypso:
        reading = await calypso.get_reading()
        reading.dump()


if __name__ == "__main__":  # pragma: nocover
    asyncio.run(calypso_read_demo())
