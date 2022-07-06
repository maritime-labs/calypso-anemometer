"""
Discover the Calypso UP10 ``ULTRASONIC`` BLE device and run a conversation on it.
License: AGPL-3.

References
==========
- https://github.com/hbldh/bleak/blob/develop/examples/discover.py
- https://github.com/hbldh/bleak/blob/develop/examples/get_services.py
- https://github.com/hbldh/bleak/blob/develop/examples/service_explorer.py
"""
import asyncio
import logging
import os
import sys
import time

from bleak import BleakClient, BleakScanner

# Configuration section.
DISCOVERY_TIMEOUT = 7.5
DEVICE_TIMEOUT = 10.0
BLUETOOTH_ADAPTER = "hci0"
DEVICE_ADDRESS = os.getenv("CALYPSO_ADDRESS")

logger = logging.getLogger()


async def find_device_address():
    """
    Find Calypso device.
    TODO: Use https://github.com/hbldh/bleak/blob/develop/examples/scanner_byname.py.
    """
    if DEVICE_ADDRESS is not None:
        return DEVICE_ADDRESS
    logger.info("Using BLE discovery to find Calypso ULTRASONIC anemometer")
    devices = await BleakScanner.discover(timeout=DISCOVERY_TIMEOUT, adapter=BLUETOOTH_ADAPTER)
    for device in devices:
        if device.name == "ULTRASONIC":
            logger.info(f"Found device: {device}")
            # Add some delay between discovery and readout. It looks like this stabilizes readings.
            time.sleep(0.5)
            return device.address
    logger.error("Unable to find device")


def get_adapter_name(client):
    if hasattr(client, "_adapter"):
        return client._adapter


async def run_conversation(device_address):
    client = BleakClient(device_address, timeout=DEVICE_TIMEOUT, adapter=BLUETOOTH_ADAPTER)
    logger.info(f"Connecting to device at {device_address} with {get_adapter_name(client)}")
    try:
        await client.connect()
        services = await client.get_services()
        for service in services:
            logger.info(f"Found service: {service}")
            for char in service.characteristics:

                logger.info(f"  Found characteristic: {char}. properties={','.join(char.properties)}")
                value = None
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        logger.exception(f"  Reading characteristic failed: {char}")
                logger.info(f"  Value: {value}")

                for descriptor in char.descriptors:
                    logger.info(f"    Found descriptor: {descriptor}")
                    value = None
                    try:
                        value = bytes(await client.read_gatt_descriptor(descriptor.handle))
                    except Exception as e:
                        logger.exception(f"    Reading descriptor failed: {descriptor}")
                    logger.info(f"    Value: {value}")

    except Exception as ex:
        # bleak.exc.BleakDBusError: [org.bluez.Error.Failed] Software caused connection abort
        # bleak.exc.BleakError: Device with address E7:B6:1B:DB:02:DF was not found.
        # futures.TimeoutError:
        logger.exception("Conversation went south")
    finally:
        logger.info("Disconnecting")
        await client.disconnect()


def setup_logging(level=logging.INFO):
    log_format = "%(asctime)-15s [%(name)-8s] %(levelname)-8s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


async def main():
    setup_logging(level=logging.INFO)
    device_address = await find_device_address()
    if device_address is None:
        sys.exit(1)
    await run_conversation(device_address)


asyncio.run(main())
