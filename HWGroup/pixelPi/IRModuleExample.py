#!/usr/bin/env python3
"""IRModuleExample1, program to practice using the IRModule

Created Apr 30, 2018"""

"""
Copyright 2018 Owain Martin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import RPi.GPIO as GPIO
import IRModule
import time
import board
import neopixel

import math
import Node
import BLE
import csv
import encoder

pixels = neopixel.NeoPixel(board.D18, 12)

Coords = (-1,-1)
ListenFlag = 1

def getNewCoords(Coords, ListenFlag):
    temp = BLE.listen()
    temp = temp.replace('_', '')
    print(temp)
    positions = encoder.decodeMessage(temp)
    #Work on this
    for i in range(len(positions)):
        if myID is positions[i][0]:
            myCoords = positions[i]
            Coords = (myCoords[1], myCoords[2])
            ListenFlag = 0
            f = open("settings.csv", "w")
            f.write(f"L,X,Y\n{ListenFlag},{Coords[0]},{Coords[1]}")
            f.close()
    return Coords

with open('settings.csv', newline='') as csvfile:
    pixels.fill(155,0,0)
    reader = csv.DictReader(csvfile)
    for row in reader:
        ListenFlag = int(row['L'])
        Coords = (int(row['X']), int(row['Y']))

while ListenFlag:
    Coords = getNewCoords(Coords)
    with open('settings.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ListenFlag = int(row['L'])
            Coords = (int(row['X']), int(row['Y']))
    print(routine)
    time.sleep(1)

delay = Coords[0]+1

pixels.fill(0,155,0)
time.sleep(4)
pixels.fill(0,0,0)

def remote_callback(code):
    global delay

    # Codes listed below are for the
    # Sparkfun 9 button remote



#16582903
#16615543
#16599223
#16591063
#16623703
#16607383
#16586983
#16619623
#16603303



    if code == 16582903:
        print('Pressed: 1')

        time.sleep(delay)
        pixels.fill((100,0,0))
        time.sleep(1)
        pixels.fill((0,0,0))
        time.sleep(3)
        pixels.fill((0,100,0))
        time.sleep(1)
        pixels.fill((0,0,0))


    elif code == 16615543:
        print('Pressed: 2')
        pixels.fill((0,100,0))
    elif code == 16599223:
        print('Pressed: 3')
        pixels.fill((0,0,100))
    elif code == 16591063:
        print('Pressed: 4')
    elif code == 16623703:
        print('Pressed: 5')
    elif code == 16607383:
        print('Pressed: 6')
    elif code == 16586983:
        print('Pressed: 7')
    elif code == 16619623:
        print('Pressed: 8')
    elif code == 16603303:
        print('Pressed: 9')
    elif code == 16593103:
        print('Pressed: 0')
        pixels.fill((255,255,255))
    elif code == 16605343:
        print('Pressed: Stop')
        pixels.fill((0,0,0))
    else:
       if code != -1:
         print(code)  # unknown code
    return

# set up IR pi pin and IR remote object
irPin = 16
ir = IRModule.IRRemote(callback='DECODE')
# using 'DECODE' option for callback will print out
# the IR code received in hexadecimal
# this can used to get the codes for whichever NEC
# compatable remote you are using

# set up GPIO options and set callback function required
# by the IR remote module (ir.pWidth)        
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
GPIO.setup(irPin,GPIO.IN)   # set irPin to input
GPIO.add_event_detect(irPin,GPIO.BOTH,callback=ir.pWidth)

ir.set_verbose(False) # verbose option prints outs high and low width durations (ms)
print('Starting IR remote ')
print('Use ctrl-c to exit program')

try:    
    time.sleep(5)

    # turn off verbose option and change callback function
    # to the function created above - remote_callback()
    print('Ready')
    ir.set_verbose(False)
    ir.set_callback(remote_callback)

    # This is where you could do other stuff
    # Blink a light, turn a motor, run a webserver
    # count sheep or mine bitcoin
    
    while True:
        time.sleep(1)

except:
    print('Removing callback and cleaning up GPIO')
    pixels.fill((0,0,0))
    ir.remove_callback()
    GPIO.cleanup(irPin)
