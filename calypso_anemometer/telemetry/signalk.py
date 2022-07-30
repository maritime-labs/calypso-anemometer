# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses
import json
import logging
import typing as t

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.model import CalypsoReading

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class SignalKDeltaItem:
    """
    Represent a SignalK Delta Format measurement item with `path` and `value` attributes.
    """

    path: str
    value: t.Union[t.AnyStr, t.SupportsInt, t.SupportsFloat, t.Dict, None]

    def asdict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SignalKDeltaMessage:
    source: str
    location: str
    items: t.Optional[t.List[SignalKDeltaItem]] = None

    def set_reading(self, reading: CalypsoReading):
        """
        Derive SignalK Delta Format update items from measurement reading.

        The path name mapping has been derived from `signalk-calypso-ultrasonic` [1]. Thanks!

        [1] https://github.com/maritime-labs/signalk-calypso-ultrasonic/blob/1.0.18/lib/calypso-ultrasonic.js#L446-L472
        """
        reading = reading.adjusted()
        self.items = [
            SignalKDeltaItem(path="environment.outside.temperature", value=reading.temperature),
            SignalKDeltaItem(path="environment.wind.angleApparent", value=reading.wind_direction),
            SignalKDeltaItem(path="environment.wind.speedApparent", value=reading.wind_speed),
            SignalKDeltaItem(path="navigation.attitude.roll", value=reading.roll),
            SignalKDeltaItem(path="navigation.attitude.pitch", value=reading.pitch),
            SignalKDeltaItem(path="navigation.attitude.yaw", value=reading.compass),
            SignalKDeltaItem(path="navigation.headingMagnetic", value=reading.compass),
            # TODO: Improve `path` naming.
            SignalKDeltaItem(path="electrical.batteries.99.name", value=self.source),
            SignalKDeltaItem(path="electrical.batteries.99.location", value=self.location),
            SignalKDeltaItem(path="electrical.batteries.99.capacity.stateOfCharge", value=reading.battery_level),
        ]

    def asdict(self):
        """
        Create message in SignalK Delta Format [1,2],

        The implementation has been derived from sensord [3] and M5StickEngineTemp [4]. Thanks!

        [1] https://github.com/SignalK/specification/blob/master/schemas/delta.json
        [2] https://github.com/SignalK/specification/blob/master/mdbook/src/data_model.md#delta-format
        [3] https://github.com/itemir/rpi_boat_utils/blob/f639653/sensord/sensord.py#L58-L63
        [4] https://github.com/andyrbarrow/M5StickEngineTemp/blob/609109d/src/tempsensor.cpp#L83-L111
        """
        data = {
            "updates": [
                {
                    "$source": CalypsoDeviceApi.NAME,
                    "values": list(map(SignalKDeltaItem.asdict, self.items)),
                },
            ]
        }
        return data

    def render(self):
        return json.dumps(self.asdict())
