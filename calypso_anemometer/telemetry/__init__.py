import logging
import typing as t

from calypso_anemometer.model import CalypsoReading
from calypso_anemometer.telemetry.common import NetworkTelemetry
from calypso_anemometer.telemetry.model import NetworkProtocol, NetworkProtocolMode, TelemetryProtocol
from calypso_anemometer.telemetry.nmea0183 import Nmea0183Messages
from calypso_anemometer.telemetry.signalk import SignalKDeltaMessage

logger = logging.getLogger(__name__)


class TelemetryAdapter:
    """
    Submit telemetry data by various means.
    """

    ACCEPTED_PROTOCOLS = [
        TelemetryProtocol.UDP_SIGNALK_DELTA,
        TelemetryProtocol.UDP_BROADCAST_NMEA0183,
    ]

    def __init__(self, uri: str):
        self._uri = None
        self.protocol = None
        self.handler: t.Union[NetworkTelemetry, None] = None

        self.uri = uri
        self.setup()

    @property
    def uri(self) -> str:
        return self._uri

    @uri.setter
    def uri(self, value):
        for accepted in self.ACCEPTED_PROTOCOLS:
            scheme = f"{accepted.value}://"
            if value.startswith(scheme):
                self._uri = value
                self.protocol = accepted
                return
        raise KeyError(f"NetworkProtocol for URI '{value}' not supported")

    def setup(self):
        host_port = self.uri.replace(f"{self.protocol.value}://", "")
        host, port = host_port.split(":")
        if self.protocol == TelemetryProtocol.UDP_SIGNALK_DELTA:
            self.handler = NetworkTelemetry(host=host, port=int(port), protocol=NetworkProtocol.UDP)
        elif self.protocol == TelemetryProtocol.UDP_BROADCAST_NMEA0183:
            self.handler = NetworkTelemetry(
                host=host, port=int(port), protocol=NetworkProtocol.UDP, mode=NetworkProtocolMode.BROADCAST
            )

    def submit(self, reading: CalypsoReading):
        if self.handler is None:
            raise KeyError("No telemetry handler established")
        if self.protocol == TelemetryProtocol.UDP_SIGNALK_DELTA:
            # TODO: Parameterize `source` and `location`.
            msg = SignalKDeltaMessage(source="Calypso UP10", location="Mast")
            msg.set_reading(reading)
            self.handler.send(msg.render())
        elif self.protocol == TelemetryProtocol.UDP_BROADCAST_NMEA0183:
            msg = Nmea0183Messages()
            msg.set_reading(reading)
            self.handler.send(msg.render())
