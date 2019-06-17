# The MIT License (MIT)
#
# Copyright (c) 2019 Gaston Williams for Sparkfun
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`sparkfun_qwiicrelay`
================================================================================

CircuitPython library for the Sparkfun QwiicRelay


* Author(s): Gaston Williams

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/fourstix/Sparkfun_CircuitPython_QwiicRelay.git"

from time import sleep
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

# public constants
QWIIC_RELAY_ADDR = const(0x18) #default I2C Address

# private constants
_RELAY_OFF = const(0x00)
_RELAY_ON = const(0x01)



_RELAY_CHANGE_ADDRESS = const(0x03)
_RELAY_VERSION = const(0x04)
_RELAY_STATUS = const(0x05)
_RELAY_NOTHING_NEW = const(0x99)

# class
class Sparkfun_QwiicRelay:
    """CircuitPython class for the Sparkfun QwiicRelay"""

    def __init__(self, i2c, address=QWIIC_RELAY_ADDR, debug=False):
        """Initialize Qwiic Relay for i2c communication."""
        self._device = I2CDevice(i2c, address)
        #save handle to i2c bus in case address is changed
        self._i2c = i2c
        self._debug = debug

# public properites

    @property
    def connected(self):
        """Check to see of the relay is available.  Returns True if successful."""
        #Attempt a connection and see if we get an error
        try:
            with self._device as device:
                pass
        except ValueError:
            return False

        return True

    @property
    def version(self):
        """Return the version string for the Relay firmware."""
        #send command to get two bytes for the version string
        version = self._command_read(_RELAY_VERSION, 2)
        # Compute major and minor values from 16-bit version
        minor = version[0] & 0xFF
        major = version[1] & 0xFF
        return 'v' + str(major) + '.' + str(minor)

    @property
    def status(self):
        """Return 1 if button pressed between reads. Button status is cleared."""
        #read button status (since last check)
        status = self._command_read(_RELAY_STATUS, 1)

        return status[0] & 0xFF


# public functions

    def on(self):
        """Turn the relay on."""
        self._command_write(_RELAY_ON)


    def off(self):
        """Turn the relay off."""
        self._command_write(_RELAY_OFF)

    def set_i2c_address(self, new_address):
        """Change the i2c address of Relay snd return True if successful."""
        # check range of new address
        if (new_address < 8 or new_address > 119):
            print('ERROR: Address outside 8-119 range')
            return False
        # write magic number 0x13 to lock register, to unlock address for update
        # self._write_register(_RELAY_I2C_LOCK, 0x13)
        # write new address
        self._write_register(_RELAY_CHANGE_ADDRESS, new_address)

	# wait a second for relay to settle after change
        sleep(1)

        # try to re-create new i2c device at new address
        try:
            self._device = I2CDevice(self._i2c, new_address)
        except ValueError as err:
            print('Address Change Failure')
            print(err)
            return False

        #if we made it here, everything went fine
        return True

# No i2c begin function is needed since I2Cdevice class takes care of that

# private functions

    def _command_read(self, command, count):
        # Send a command then read count number of bytes.
        with self._device as device:
            device.write(bytes([command]), stop=False)
            result = bytearray(count)
            device.readinto(result)
            if self._debug:
                print("$%02X => %s" % (command, [hex(i) for i in result]))
            return result

    def _command_write(self, command):
        # Send a byte command to the device
        with self._device as device:
            device.write(bytes([command & 0xFF]))
            if self._debug:
                print("$%02X" % (command))

    def _write_register(self, addr, value):
        # Write a byte to the specified 8-bit register address
        with self._device as device:
            device.write(bytes([addr & 0xFF, value & 0xFF]))
            if self._debug:
                print("$%02X <= 0x%02X" % (addr, value))

