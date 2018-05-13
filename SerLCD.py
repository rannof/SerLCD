#!/usr/bin/env python
#
# Libary for SerLCD v2.5 Controller
# by Robert Postill <rpostill@gmail.com>
#
# Currently support only 16x2 LCD
#
# Update by Ran N. Nof @ GSI, 2018
# <ran.nof@gmail.com>

import serial
import time

class SerLCD:
    # Display Commands to enter command mode
    COMMAND1 = 254
    COMMAND2 = 124
    # LCD Type setup (not fully supported)
    CHARWIDTH20 = 3
    CHARWIDTH16 = 5
    LINES4 = 5
    LINES2 = 6
    # Extended LCD Commands
    CLEARDISPLAY = 01
    MOVERIGHT = 20
    MOVELEFT = 16
    SCROLLRIGHT = 28
    SCROLLLEFT = 24
    DISPLAYON = 12
    DISPLAYOFF = 8
    BLINKON = 13  
    BLINKOFF = 12
    POSITION = 128
    # Other options
    SPLASHTOGGLE = 9
    SETSPLASH = 10

    def __init__(self, port="/dev/ttyAMA0", baud="9600"):
        self.lcd = serial.Serial(port=port,baudrate=baud)

    def __del__(self):
        self.lcd.close()

    def clear(self):
        self.write(chr(self.COMMAND1))
        self.write(chr(self.CLEARDISPLAY))

    def pos(self,x,y):
        self.position = 0
        if x == 1:
            self.position = y - 1
        elif x == 2:
            self.position = y + 63
        self.position = self.position + 128
        self.write(chr(self.COMMAND1))
        self.write(chr(self.position))

    def write(self,text):
        if self.lcd.isOpen():
            self.lcd.write(text)
        else:
            raise IOError, "Serial port is closed"

    def display(self,x):
        if x == 0:
            self.write(chr(self.COMMAND1))
            self.write(chr(self.DISPLAYOFF))
        else:
            self.write(chr(self.COMMAND1))
            self.write(chr(self.DISPLAYON))

    def scroll_right(self):
        self.write(chr(self.COMMAND1))
        self.write(chr(self.SCROLLRIGHT))

    def scroll_left(self):
        self.write(chr(self.COMMAND1))
        self.write(chr(self.SCROLLLEFT))

    def move_right(self):
        self.write(chr(self.COMMAND1))
        self.write(chr(self.MOVERIGHT))

    def move_left(self):
        self.write(chr(self.COMMAND1))
        self.write(chr(self.MOVELEFT))

    def blink(self, x):
      if x == 1:
          self.write(chr(self.COMMAND1))
          self.write(chr(self.BLINKON))
      else:
          self.write(chr(self.COMMAND1))
          self.write(chr(self.BLINKOFF))

    def splash_set(self, line1, line2):
        self.pos(1, 1)
        self.write("                ")   # We want to write blanks to all
        self.pos(2, 1)                   # lines to prevent bug in firmware
        self.write("                ")   # where old text can appear
        self.clear()
        self.screen(line1, line2)
        time.sleep(1)
        self.write(chr(self.COMMAND2))
        self.write(chr(self.SETSPLASH))
        time.sleep(1)
        self.clear()

    def splash_toggle(self):
        self.write(chr(self.COMMAND2))
        self.write(chr(self.SPLASHTOGGLE))

    def bright_level(self, x):
        if not 30 >= x >= 1:
            raise ValueError, "Brightness value can be 1 - 30"
        self.brightness = x + 127
        self.write(chr(self.COMMAND1))
        self.write(chr(self.brightness))

    def screen(self, line1, line2):
        self.clear()
        self.write(line1)
        self.pos(2, 1)
        self.write(line2)

if __name__ == "__main__":
    display = SerLCD()
    display.clear()
    display.write(" Python Serial ")
    display.pos(2,1)
    display.write("LCD Library v0.2")
