# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import pytest
from pytest_mock import MockerFixture

from calypso_anemometer.core import CalypsoDeviceApi


@pytest.fixture(autouse=True)
def use_stable_cross_platform_bluetooth_adapter(mocker: MockerFixture):
    """
    Make sure the tests will always use the designated bluetooth adapter.
    Otherwise, the outcome will deviate on Linux vs. macOS.
    """
    mocker.patch("calypso_anemometer.core.get_adapter_name", return_value=CalypsoDeviceApi.BLUETOOTH_ADAPTER)
