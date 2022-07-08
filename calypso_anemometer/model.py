import dataclasses
from typing import Optional


@dataclasses.dataclass
class BleCharSpec:
    name: str
    uuid: str


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
