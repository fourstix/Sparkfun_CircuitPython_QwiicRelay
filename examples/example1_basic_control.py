#  This is example is for the SparkFun Qwiic Single Relay.
#  SparkFun sells these at its website: www.sparkfun.com
#  Do you like this library? Help support SparkFun. Buy a board!
#  https://www.sparkfun.com/products/15093

"""
 Qwiic Relay Example 1 - example1_basic_control.py
 Written by Gaston Williams, June 13th, 2019
 Based on Arduino code written by
 Kevin Kuwata @ SparkX, March 21, 2018
 The Qwiic Single Relay is an I2C controlled relay produced by sparkfun

 Example 1 - Basic Control:
 This program uses the Qwiic Relay CircuitPython Library to
 control the Qwiic Relay breakout over I2C and demonstrate
 basic functionality.
"""

from time import sleep
import board
import busio
import sparkfun_qwiicrelay

# Create bus object using our board's I2C port
i2c = busio.I2C(board.SCL, board.SDA)

# Create relay object
relay = sparkfun_qwiicrelay.Sparkfun_QwiicRelay(i2c)

print('Qwicc Relay Example 1 Basic Control')

# Check if connected
if relay.connected:
    print('Relay connected.')
else:
    print('Relay does not appear to be connected. Please check wiring.')
    exit()

print('Type Ctrl-C to exit program.')

try:
    while True:
        relay.on()
        sleep(2)
        relay.off()
        sleep(2)

except KeyboardInterrupt:
    pass
