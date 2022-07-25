####################
Sandbox installation
####################


************
Introduction
************

It is recommended to use a Python virtualenv. The ``make test`` command
provided through the repository will automatically install a Python
virtualenv into the ``.venv`` directory.


*****
Usage
*****
::

    git clone https://github.com/maritime-labs/calypso-anemometer
    cd calypso-anemometer
    make test


*****
Notes
*****

Random notes about CLI entrypoints suitable for development.

::

    # Set device data rate to one of HZ_1, HZ_4, or HZ_8.
    # Note: Works only for the upcoming conversation. Will be back at HZ_4 afterwards.
    calypso-anemometer set-option --rate=hz_1

    # Set device mode to one of SLEEP, LOW_POWER, or NORMAL.
    # Note: Does not work, the setting is read-only.
    calypso-anemometer set-option --mode=normal

    # Explore all services and characteristics. Useful for debugging purposes.
    calypso-anemometer explore
