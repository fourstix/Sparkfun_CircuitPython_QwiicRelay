#  This is example is for the SparkFun Qwiic Single Relay.
#  SparkFun sells these at its website: www.sparkfun.com
#  Do you like this library? Help support SparkFun. Buy a board!
#  https://www.sparkfun.com/products/15093

"""
  Qwiic Relay Example 3 - example3_i2c_Scanner.py
  Written by Gaston Williams, June 17th, 2019
  The Qwiic Single Relay is an I2C controlled relay produced by sparkfun

  Example 3 - I2C Scanner
  This progam uses CircuitPython BusIO library to find the current
  address of the Qwiic Relay. It uses the I2C Scanner Example from
  https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/i2c-devices

  The factory default address is 0x18.
"""

import time

import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

# For some reason i2c.scan() returns all addresses above the relay address
# So we will manually look for the really address

def test_i2c_address(addr):
    "test an address to see if there's a device there"""
    while not i2c.try_lock():
        pass

    try:
        i2c.writeto(addr, b'')
    except OSError:
        # some OS's dont like writing an empty bytesting...
        # Retry by reading a byte
        try:
            result = bytearray(1)
            i2c.readfrom_into(addr, result)
        except OSError:
                return False
        finally:
            i2c.unlock()

    return True


addresses = []

for address in range(0x08, 0x80):
    if(test_i2c_address(address)):
        print('Found relay at address ' + hex(address))
        exit()

print('No I2C device found.')


