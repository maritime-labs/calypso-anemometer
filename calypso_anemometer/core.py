# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
"""
Discover the Calypso UP10 ultrasonic BLE device and run a conversation on it.

References
==========
- https://github.com/hbldh/bleak/blob/develop/examples/discover.py
- https://github.com/hbldh/bleak/blob/develop/examples/get_services.py
- https://github.com/hbldh/bleak/blob/develop/examples/service_explorer.py
- https://github.com/hbldh/bleak/blob/develop/examples/scanner_byname.py
"""
import asyncio
import concurrent
import logging
from typing import Callable, Optional

from bleak import BleakClient, BleakError, BleakScanner

from calypso_anemometer.exception import (
    BluetoothAdapterError,
    BluetoothConversationError,
    BluetoothDiscoveryError,
    BluetoothTimeoutError,
    CalypsoDecodingError,
)
from calypso_anemometer.model import (
    BleCharSpec,
    CalypsoDeviceDataRate,
    CalypsoDeviceInfo,
    CalypsoDeviceInfoCharacteristic,
    CalypsoDeviceMode,
    CalypsoDeviceReadingCharacteristic,
    CalypsoDeviceStatus,
    CalypsoDeviceStatusCharacteristic,
    CalypsoReading,
    Settings,
)
from calypso_anemometer.util import to_json

logger = logging.getLogger(__name__)


class CalypsoDeviceApi:

    NAME = "calypso-up10"
    DESCRIPTION = "Calypso UP10 anemometer"
    BLUETOOTH_DEVICE_NAME = "ULTRASONIC"

    DEVICE_INFO_CHARACTERISTICS = [
        CalypsoDeviceInfoCharacteristic.manufacturer_name,
        CalypsoDeviceInfoCharacteristic.model_number,
        CalypsoDeviceInfoCharacteristic.serial_number,
        CalypsoDeviceInfoCharacteristic.hardware_revision,
        CalypsoDeviceInfoCharacteristic.firmware_revision,
        CalypsoDeviceInfoCharacteristic.software_revision,
    ]
    DEVICE_STATUS_CHARACTERISTICS = [
        CalypsoDeviceStatusCharacteristic.mode,
        CalypsoDeviceStatusCharacteristic.rate,
        CalypsoDeviceStatusCharacteristic.compass,
    ]

    def __init__(self, settings: Optional[Settings] = None, ble_address: Optional[str] = None):
        if settings is None:
            settings = Settings(ble_address=ble_address)
        self.settings = settings
        self.ble_address = settings.ble_address
        self.client: BleakClient

        logger.info(f"Initializing client with {self.settings}")

    async def __aenter__(self):

        if self.ble_address is None:
            if not await self.discover():
                raise BluetoothDiscoveryError(f"Unable to discover device {self.DESCRIPTION}")

        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
        if exc_val is not None:  # pragma: no cover
            raise exc_val

    async def discover(self, force=False) -> bool:
        """
        Discover device via BLE.
        """

        # Skip discovery when already discovered and not forced.
        if self.ble_address is not None and not force:
            return True

        logger.info(f"Using BLE discovery to find {self.DESCRIPTION}")
        try:
            device = await BleakScanner.find_device_by_filter(
                filterfunc=lambda d, ad: d.name == self.BLUETOOTH_DEVICE_NAME,
                timeout=self.settings.ble_discovery_timeout,
                adapter=self.settings.ble_adapter,
            )
        except BleakError as ex:
            message = f"{ex.__class__.__name__}: {ex}"
            if "Bluetooth device is turned off" in message:
                raise BluetoothAdapterError(message) from None
            else:
                raise

        if device is not None:
            self.ble_address = device.address
            logger.info(f"Found device at address: {device}")
            return True
        else:
            logger.error("Unable to find device")
            return False

    async def connect(self):
        self.client = BleakClient(
            self.ble_address, timeout=self.settings.ble_connect_timeout, adapter=self.settings.ble_adapter
        )
        logger.info(f"Connecting to device at '{self.ble_address}' with adapter '{get_adapter_name(self.client)}'")
        try:
            await self.client.connect()
        except BleakError as ex:
            message = f"{ex.__class__.__name__}: {ex}"
            logger.error(f"Conversation went south: {message}")
            if "Bluetooth device is turned off" in message:
                raise BluetoothAdapterError(message) from None
            else:
                raise BluetoothConversationError(message) from None
        except (concurrent.futures.TimeoutError, asyncio.TimeoutError) as ex:
            message = f"{ex.__class__.__name__}: {ex}"
            logger.error(message)
            raise BluetoothTimeoutError(message)
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
        - bleak.exc.BleakError: Device with address F8:C7:2C:EC:13:D0 was not found.
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
                    except Exception:
                        logger.exception(f"  Reading characteristic failed: {char}")
                logger.info(f"  Value: {value}")

                for descriptor in char.descriptors:
                    logger.info(f"    Found descriptor: {descriptor}")
                    value = None
                    try:
                        value = bytes(await self.client.read_gatt_descriptor(descriptor.handle))
                    except Exception:
                        logger.exception(f"    Reading descriptor failed: {descriptor}")
                    logger.info(f"    Value: {value}")

    async def about(self):
        response = {
            "info": await self.get_info(),
            "status": (await self.get_status()).aslabeldict(),
        }
        print(to_json(response))

    async def get_info(self) -> CalypsoDeviceInfo:
        logger.info("Getting device information")
        data = {}
        for charspec_item in self.DEVICE_INFO_CHARACTERISTICS:
            charspec: BleCharSpec = charspec_item.value
            value = (await self.client.read_gatt_char(charspec.uuid)).decode()
            data[charspec.name] = value
        return CalypsoDeviceInfo(ble_address=self.ble_address, **data)

    async def get_status(self) -> CalypsoDeviceStatus:
        logger.info("Getting status information")
        status = CalypsoDeviceStatus()
        for charspec_item in self.DEVICE_STATUS_CHARACTERISTICS:
            charspec: BleCharSpec = charspec_item.value
            rawvalue: bytearray = await self.client.read_gatt_char(charspec.uuid)
            value: int = rawvalue[0]
            if isinstance(charspec.decoder, Callable):
                value = charspec.decoder(value)
            setattr(status, charspec.name, value)
        return status

    async def set_mode(self, mode: CalypsoDeviceMode):
        logger.info(f"Setting device mode to {mode}")
        await self.client.write_gatt_char(
            CalypsoDeviceStatusCharacteristic.mode.value.uuid, data=bytes([mode.value]), response=True
        )

    async def set_datarate(self, rate: CalypsoDeviceDataRate):
        logger.info(f"Setting data rate to {rate}")
        await self.client.write_gatt_char(
            CalypsoDeviceStatusCharacteristic.rate.value.uuid, data=bytes([rate.value]), response=True
        )

    async def get_reading(self):
        logger.info("Requesting reading")
        data: bytearray = await self.client.read_gatt_char(CalypsoDeviceReadingCharacteristic.data.value.uuid)
        reading = self.decode_reading(data)
        self.on_reading(reading)
        return reading

    async def subscribe_reading(self, callback: Optional[Callable] = None):
        logger.info("Subscribing to readings")
        callback = callback or self.on_reading

        async def handler(sender: int, data: bytearray):
            reading = self.decode_reading(data, sender=sender)
            callback(reading)

        await self.client.start_notify(CalypsoDeviceReadingCharacteristic.data.value.uuid, handler)

    async def unsubscribe_reading(self):
        logger.info("Unsubscribing from readings")
        await self.client.stop_notify(CalypsoDeviceReadingCharacteristic.data.value.uuid)

    @staticmethod
    def decode_reading(data: bytearray, sender: Optional[int] = None):
        logger.debug(f"Received buffer:  {data}")
        try:
            reading = CalypsoReading.from_buffer(data)
        except Exception as ex:
            msg = f"Decoding reading failed. Reason: {ex}. Data: {data}"
            logger.exception(msg)
            raise CalypsoDecodingError(msg)
        logger.debug(f"Decoded reading: {reading}")
        return reading

    def on_reading(self, reading: CalypsoReading):
        pass

    async def read_characteristic_string(self, characteristic_id: str) -> str:
        logger.info(f"Reading the characteristic {characteristic_id} as string")
        char = await self.client.read_gatt_char(characteristic_id)
        return char.decode()


def get_adapter_name(client):
    if hasattr(client, "_adapter"):
        return client._adapter
