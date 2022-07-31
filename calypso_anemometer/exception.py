# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3


class CalypsoError(Exception):
    pass


class CalypsoDecodingError(CalypsoError):
    pass


class BluetoothAdapterError(CalypsoError):
    pass


class BluetoothDiscoveryError(CalypsoError):
    pass


class BluetoothConversationError(CalypsoError):
    pass


class BluetoothTimeoutError(CalypsoError):
    pass
