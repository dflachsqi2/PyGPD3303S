# GPDX303S
Python interface for GPD-x303S power supplies by GW Instek

## Requirements
- PySerial
- rich (optional)

## Installation
```
$ pip install gpdx303s
```

If you are using Anaconda, try the command below instead.
```
$ pip install -i https://pypi.anaconda.org/oxon/simple gpdx303s
```

## Device Driver
GPD-X303S uses a USB to serial converter chip provided by FTDI. If you have not
installed its device driver, please download and install it on your machine
first.

macOS and most Linux distributions support FTDI chips without installing a device driver.

## Example

    >>> import gpdx303s
    >>> gpd = gpdx303s.GPDX303S()
    >>> gpd.open('/dev/ttyUSB0') # Open the device
    >>> gpd.setVoltage(1, 1.234) # Set the voltage of channel 1 to 1.234 (V)
    >>> gpd.enableOutput(True) # Output ON
    >>> v = gpd.getVoltageOutput(1) # read the actual voltage
