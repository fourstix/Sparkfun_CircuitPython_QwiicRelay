#  This is example is for the SparkFun Qwiic Relay.
#  SparkFun sells these at its website: www.sparkfun.com
#  Do you like this library? Help support SparkFun. Buy a board!
#  https://www.sparkfun.com/products/15168

"""
 Qwiic Relay Simple Test - qwiicrelay_simpletest.py
 Written by Gaston Williams, June 13th, 2019
 The Qwiic Relay is a I2C controlled analog relay

 Simple Test:
 This program uses the Qwiic Relay CircuitPython Library to read
 and print out the relay position.
"""

import board
import busio
import sparkfun_qwiicrelay

# Create bus object using our board's I2C port
i2c = busio.I2C(board.SCL, board.SDA)

# Create relay object
relay = sparkfun_qwiicrelay.Sparkfun_QwiicRelay(i2c)

# Check if connected
if relay.connected:
    print('Relay connected.')
else:
    print('Relay does not appear to be connected. Please check wiring.')
