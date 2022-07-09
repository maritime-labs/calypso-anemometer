import dataclasses
import logging
import struct
from enum import Enum, IntEnum
from typing import Optional, Union

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class BleCharSpec:
    name: str
    uuid: str
    decoder: Optional[Union[Enum]] = None


@dataclasses.dataclass
class CalypsoDeviceInfo:
    ble_address: str
    manufacturer_name: str
    model_number: str
    serial_number: str
    hardware_revision: Optional[str]
    firmware_revision: Optional[str]
    software_revision: Optional[str]

    def asdict(self):
        return dataclasses.asdict(self)


class CalypsoDeviceMode(IntEnum):
    SLEEP = 0x00
    LOW_POWER = 0x01
    NORMAL = 0x02


class CalypsoDeviceDataRate(IntEnum):
    HZ_1 = 0x01
    HZ_4 = 0x04
    HZ_8 = 0x08


class CalypsoDeviceCompassStatus(IntEnum):
    OFF = 0x00
    ON = 0x01


@dataclasses.dataclass
class CalypsoDeviceStatus:
    mode: Optional[CalypsoDeviceMode] = None
    rate: Optional[CalypsoDeviceDataRate] = None
    compass: Optional[CalypsoDeviceCompassStatus] = None

    def aslabeldict(self):
        return {
            "mode": self.mode.name,
            "rate": self.rate.name,
            "compass": self.compass.name,
        }
