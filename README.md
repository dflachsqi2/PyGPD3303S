# GPDX303S
Python interface for GPD-x303S power supplies by GW Instek

## Requirements
- PySerial
- rich (optional)

## Installation
Clone this repo and
```
$ git clone https://github.com/dflachsqi2/PyGPD3303S.git
$ cd PyGPD3303S
$ pip3 install .    
# or python3 setup.py install
# this isn't in pypi so
# pip install gpdx303s
```

## Example

    >>> import gpdx303s
    >>> gpd = gpdx303s.GPDX303S()
    >>> gpd.open('/dev/ttyUSB0') # Open the device
    >>> gpd.setVoltage(1, 1.234) # Set the voltage of channel 1 to 1.234 (V)
    >>> gpd.enableOutput(True) # Output ON
    >>> v = gpd.getVoltageOutput(1) # read the actual voltage
