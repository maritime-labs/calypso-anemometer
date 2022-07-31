################
Production notes
################


***************************
Multiple Bluetooth adapters
***************************

If your system sports multiple Bluetooth adapters, you might want to select the
right one to use with the program.

For that purpose, you can use the ``--ble-adapter`` command line option, like::

    calypso-anemometer info --ble-adapter=hci1
    calypso-anemometer read --ble-adapter=hci1

Alternatively, you can use the ``CALYPSO_BLE_ADAPTER`` environment variable, like::

    export CALYPSO_BLE_ADAPTER=hci1
    calypso-anemometer info

In order to use the default again, use::

    unset CALYPSO_BLE_ADAPTER


*************************************
Device discovery vs. multiple devices
*************************************

By default, the program will look for any BLE device called ``ULTRASONIC``
and will attempt to connect to the first one discovered.

While this will probably work in most environments, there is still a chance that
multiple devices with the same name are around and you will be connecting to the
wrong device. This scenario also applies when you are using multiple devices on
your own site.

In this case, make sure to shortcut the device discovery procedure by addressing
the BLE peripheral directly. For that purpose, you can use the ``--ble-address``
command line option, like::

    calypso-anemometer info --ble-address=F8:C7:2C:EC:13:D0
    calypso-anemometer read --ble-address=F8:C7:2C:EC:13:D0

Alternatively, you can use the ``CALYPSO_BLE_ADDRESS`` environment variable, like::

    # Linux
    export CALYPSO_BLE_ADDRESS=F8:C7:2C:EC:13:D0
    calypso-anemometer info

    # macOS
    export CALYPSO_BLE_ADDRESS=0C3E4A46-BFCB-52E5-BC57-DE1D60C3A2B2
    calypso-anemometer info

In order to activate automatic device discovery again, invoke::

    unset CALYPSO_BLE_ADDRESS


*************************
Suppress output to STDOUT
*************************

The ``--quiet`` option will silence anything printed to STDOUT. You can exercise this
option by trying the command::

    calypso-anemometer --quiet fake --subscribe --rate=hz_8

Alternatively, you can also use the ``CALYPSO_QUIET`` environment variable::

    export CALYPSO_QUIET=true
    calypso-anemometer fake --subscribe --rate=hz_8


*********************
Run as system service
*********************

TODO: ``systemd`` configuration needed.



*******************
Save power at night
*******************

TODO: ``systemd`` configuration snippets which stop the service at night.
