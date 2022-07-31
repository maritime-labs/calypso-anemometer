# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import os

import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def use_stable_cross_platform_bluetooth_adapter(mocker: MockerFixture):
    """
    Make sure the tests will always use the designated bluetooth adapter.
    Otherwise, the outcome will deviate on Linux vs. macOS.
    """
    mocker.patch("calypso_anemometer.core.get_adapter_name", return_value="hci0")


@pytest.fixture(autouse=True)
def clean_environment_variables(mocker: MockerFixture):
    """
    Make sure the tests will run with a deterministic set of application-specific environment variables.
    """
    mocker.patch.dict(os.environ, {"CALYPSO_QUIET": "false"})
