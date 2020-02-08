#!/usr/bin/env python
# libraries
import time

import RPi.GPIO as GPIO

# Use BCM GPIO references
# Instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO signals to use Pins 18,22,24,26 GPIO24,GPIO25,GPIO8,GPIO7
StepPins = [24, 25, 8, 7]


def init_pin(pinid):
    print "Setup pins {}".format(pinid)
    GPIO.setup(pinid, GPIO.OUT)
    GPIO.output(pinid, False)


def release_pin(pinid):
    print "Cleanup pins {}".format(pinid)
    GPIO.output(pin, False)
    GPIO.cleanup(pinid)


# Set all pins as output
for pin in StepPins:
    init_pin(pin)


# Define some settings
WaitTime = 0.002

# Define simple sequence
Seq1 = [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]

# Define advanced half-step sequence
Seq2 = [[1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]]

# Choose a sequence to use
Seq = Seq1
StepCount = len(Seq)


def steps(nb, direction):
    stepcounter = 0
    print("nbsteps {} and direction {}".format(nb, direction))
    for i in range(nb):
        flush_gpio_for_seq(stepcounter)
        stepcounter += direction
        # If we reach the end of the sequence
        # start again
        if stepcounter >= StepCount:
            stepcounter = 0
        if stepcounter < 0:
            stepcounter = StepCount - 1
        # Wait before moving on
        time.sleep(WaitTime)


def flush_gpio_for_seq(seq_number):
    print " Enable GPIO sequence {}".format(seq_number)
    for pin in range(4):
        xpin = StepPins[pin]
        if Seq[seq_number][pin] != 0:
            GPIO.output(xpin, True)
        else:
            GPIO.output(xpin, False)


# Start main loop
nbStepsPerRev = 2048
hasRun = False
while not hasRun:
    steps(nbStepsPerRev, 1)  # parcourt un tour dans le sens horaire
    time.sleep(1)
    steps(nbStepsPerRev, -1)  # parcourt un tour dans le sens anti-horaire
    time.sleep(1)
    hasRun = True
print "Stop motor"


for pin in StepPins:
    release_pin(pin)
