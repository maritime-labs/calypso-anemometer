import typing as t

from calypso_anemometer.model import CalypsoReading
from calypso_anemometer.telemetry.model import NetworkProtocol, TelemetryProtocol
from calypso_anemometer.telemetry.signalk import SignalKDeltaMessage, SignalKTelemetry


class TelemetryAdapter:
    """
    Submit telemetry data by various means.
    """

    ACCEPTED_PROTOCOLS = [
        TelemetryProtocol.UDP_SIGNALK_DELTA,
    ]

    def __init__(self, uri: str):
        self._uri = None
        self.protocol = None
        self.handler: t.Union[SignalKTelemetry, None] = None

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
        if self.protocol == TelemetryProtocol.UDP_SIGNALK_DELTA:
            host_port = self.uri.replace(f"{self.protocol.value}://", "")
            print("host_port:", host_port)
            host, port = host_port.split(":")
            self.handler = SignalKTelemetry(host=host, port=int(port), protocol=NetworkProtocol.UDP)

    def submit(self, reading: CalypsoReading):
        if self.handler is None:
            raise KeyError("No telemetry handler established")
        if self.protocol == TelemetryProtocol.UDP_SIGNALK_DELTA:
            # TODO: Parameterize `source` and `location`.
            msg = SignalKDeltaMessage(source="Calypso UP10", location="Mast")
            msg.set_reading(reading)
            self.handler.submit(msg.asdict())
