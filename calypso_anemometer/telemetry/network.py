# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import socket

from calypso_anemometer.telemetry.model import NetworkProtocol, NetworkProtocolMode

logger = logging.getLogger(__name__)


class NetworkTelemetry:
    """
    Submit telemetry data over TCP or UDP.
    """

    def __init__(
        self,
        host: str,
        port: int,
        protocol: NetworkProtocol = NetworkProtocol.UDP,
        mode: NetworkProtocolMode = NetworkProtocolMode.UNICAST,
    ):
        self.host = host
        self.port = port
        self.protocol = protocol
        if self.protocol == NetworkProtocol.TCP:
            self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        elif self.protocol == NetworkProtocol.UDP:
            self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        if mode == NetworkProtocolMode.BROADCAST:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    def send(self, payload: str, newline=True):
        logger.info(f"Sending message to {self.protocol.value}://{self.host}:{self.port}. {payload}")
        address = (self.host, self.port)
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        if newline:
            payload += b"\n"
        if self.protocol == NetworkProtocol.TCP:
            self.socket.connect(address)
            self.socket.send(payload)
            self.socket.close()
        elif self.protocol == NetworkProtocol.UDP:
            self.socket.sendto(payload, address)
