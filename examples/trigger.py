#!/usr/bin/env python
from SerLCD.SerLCD import SerLCD
from datetime import datetime
import RPi.GPIO as GPIO
import time
import logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level='DEBUG')
INCHANNEL = 16
OUTCHANNEL = 18
log = logging.getLogger('trigger')
PITYPE = GPIO.RPI_INFO['TYPE']
if not 'Pi' in PITYPE:
    PITYPE = 'Pi1 '+PITYPE

class TRIGGER(object):
    def __init__(self,inchannel=INCHANNEL, outchannel=OUTCHANNEL):
        log.debug('Input Channel: {} ; Output Channel: {}'.format(inchannel,outchannel))
        log.debug('RaspberryPi version: {}'.format(PITYPE))
        self.triggers = []
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(outchannel, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(inchannel, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        self.display = SerLCD()
        self.display.clear()
        self.display.screen(PITYPE, 'Trigger Standby.')
        GPIO.add_event_detect(inchannel, GPIO.RISING, callback=self.trigger, bouncetime=300)

    def trigger(self, channel):
        t = datetime.utcnow()
        if GPIO.input(INCHANNEL):
            self.triggers.append(t)
            log.debug('GPIO {} Triggered: {}'.format(channel,t.isoformat()))
            text = '{:15s} {:15s}'.format(*self.triggers[-1].isoformat().split('T'))
            self.display.clear()
            self.display.write(text)

    def test(self, channel=OUTCHANNEL):
        GPIO.output(channel,1)
        t = datetime.utcnow()
        time.sleep(0.001)
        GPIO.output(channel,0)
        if len(self.triggers):
            log.debug('GPIO {} Trigger test: {} ({})'.format(channel, t.isoformat(), (self.triggers[-1]-t)))
        else:
            log.error('GPIO {} Trigger test: {} FAILED!'.format(channel,t.isoformat()))


if __name__ == '__main__':
    self = TRIGGER()
    time.sleep(1)
    self.test()
    raw_input('Done? ')
    GPIO.cleanup()
