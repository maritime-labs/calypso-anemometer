"""
Discover the Calypso UP10 ``ULTRASONIC`` BLE device and run a conversation on it.
License: AGPL-3.

References
==========
- https://github.com/hbldh/bleak/blob/develop/examples/discover.py
- https://github.com/hbldh/bleak/blob/develop/examples/get_services.py
- https://github.com/hbldh/bleak/blob/develop/examples/service_explorer.py
"""
import concurrent
import logging
import time
from typing import Optional

from bleak import BleakClient, BleakError, BleakScanner

from calypso_anemometer.exception import BluetoothAdapterError, BluetoothConversationError, BluetoothDiscoveryError

# Configuration section.
DISCOVERY_TIMEOUT = 7.5
DEVICE_TIMEOUT = 10.0
BLUETOOTH_ADAPTER = "hci0"

logger = logging.getLogger()


class CalypsoDeviceApi:

    NAME = "calypso-up10"
    DESCRIPTION = "Calypso UP10 anemometer"

    def __init__(self, ble_address: Optional[str] = None):
        self.ble_address = ble_address
        self.client: BleakClient = None

    async def __aenter__(self):

        if self.ble_address is None:
            if not await self.discover():
                raise BluetoothDiscoveryError(
                    f"Unable to discover device {self.DESCRIPTION}"
                )

        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
        if exc_val is not None:
            raise exc_val

    async def discover(self, force=False) -> bool:
        """
        Discover device via BLE.
        TODO: Use https://github.com/hbldh/bleak/blob/develop/examples/scanner_byname.py.
        """
        # Skip discovery when already discovered and not forced.
        if self.ble_address is not None and not force:
            return True

        logger.info(f"Using BLE discovery to find {self.DESCRIPTION}")
        try:
            devices = await BleakScanner.discover(timeout=DISCOVERY_TIMEOUT, adapter=BLUETOOTH_ADAPTER)
        except BleakError as ex:
            message = f"{ex.__class__.__name__}: {ex}"
            if "Bluetooth device is turned off" in message:
                raise BluetoothAdapterError(message) from None
        for device in devices:
            if device.name == "ULTRASONIC":
                logger.info(f"Found device at address: {device}")
                # Add some delay between discovery and readout. It looks like this stabilizes readings.
                time.sleep(0.5)
                self.ble_address = device.address
                return True
        logger.error("Unable to find device")
        return False

    async def connect(self):
        self.client = BleakClient(self.ble_address, timeout=DEVICE_TIMEOUT, adapter=BLUETOOTH_ADAPTER)
        logger.info(f"Connecting to device at {self.ble_address} with adapter {get_adapter_name(self.client)}")
        try:
            await self.client.connect()
        except (BleakError, concurrent.futures.TimeoutError) as ex:
            message = f"{ex.__class__.__name__}: {ex}"
            logger.error(f"Conversation went south: {message}")
            if "Bluetooth device is turned off" in message:
                raise BluetoothAdapterError(message) from None
            else:
                raise BluetoothConversationError(message) from None
        # finally:
        #    logger.info("Disconnecting")
        #    await self.disconnect()

    async def disconnect(self):
        logger.info("Disconnecting")
        try:
            await self.client.disconnect()
        except Exception:
            logger.exception("Disconnect failed")

    async def explore(self):
        """
        Explore all services and characteristics. Useful for debugging purposes.

        Possible errors:

        - bleak.exc.BleakDBusError: [org.bluez.Error.Failed] Software caused connection abort
        - bleak.exc.BleakError: Device with address E7:B6:1B:DB:02:DF was not found.
        - futures.TimeoutError:
        """
        services = await self.client.get_services()
        for service in services:
            logger.info(f"Found service: {service}")
            for char in service.characteristics:

                logger.info(f"  Found characteristic: {char}. properties={','.join(char.properties)}")
                value = None
                if "read" in char.properties:
                    try:
                        value = bytes(await self.client.read_gatt_char(char.uuid))
                    except Exception as e:
                        logger.exception(f"  Reading characteristic failed: {char}")
                logger.info(f"  Value: {value}")

                for descriptor in char.descriptors:
                    logger.info(f"    Found descriptor: {descriptor}")
                    value = None
                    try:
                        value = bytes(await self.client.read_gatt_descriptor(descriptor.handle))
                    except Exception as e:
                        logger.exception(f"    Reading descriptor failed: {descriptor}")
                    logger.info(f"    Value: {value}")

    async def get_info(self):
        data = {}
        ch = await self.client.read_gatt_char("00002a29-0000-1000-8000-00805f9b34fb")
        data["manufacturer"] = ch.decode()
        ch = await self.client.read_gatt_char("00002a24-0000-1000-8000-00805f9b34fb")
        data["model_number"] = ch.decode()
        ch = await self.client.read_gatt_char("00002a25-0000-1000-8000-00805f9b34fb")
        data["serial_number"] = ch.decode()
        ch = await self.client.read_gatt_char("00002a26-0000-1000-8000-00805f9b34fb")
        data["firmware_revision"] = ch.decode()
        return data


def get_adapter_name(client):
    if hasattr(client, "_adapter"):
        return client._adapter
