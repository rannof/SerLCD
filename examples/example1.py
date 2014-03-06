#!/usr/bin/env python
from SerLCD2 import SerLCD
import time
from array import *

# Initalize display
display = SerLCD("/dev/ttyAMA0","9600")

# Clear screen
display.clear

# Example output
a = ["Example 1", "On Line2"]
display.screen(a[0], a[1])
