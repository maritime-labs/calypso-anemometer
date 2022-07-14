import logging
import socket

from calypso_anemometer.telemetry.model import NetworkProtocol

logger = logging.getLogger(__name__)


class NetworkTelemetry:
    """
    Submit telemetry data over TCP or UDP.
    """

    def __init__(self, host: str, port: int, protocol: NetworkProtocol = NetworkProtocol.UDP):
        self.host = host
        self.port = port
        self.protocol = protocol
        if self.protocol == NetworkProtocol.TCP:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.protocol == NetworkProtocol.UDP:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, payload: str):
        logger.info(f"Sending message to {self.protocol.value}://{self.host}:{self.port}. {payload}")
        address = (self.host, self.port)
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        if self.protocol == NetworkProtocol.TCP:
            self.socket.connect(address)
            self.socket.send(payload)
            self.socket.close()
        elif self.protocol == NetworkProtocol.UDP:
            self.socket.sendto(payload, address)
