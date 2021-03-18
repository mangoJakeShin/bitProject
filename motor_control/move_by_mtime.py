import time
import RPi.GPIO as GPIO
import os
import datetime

PUL = 24
DIR = 23
ENA = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
print("initialization completed")

delay_a = 0.001
delay_b = 0.0005

cycles = 10
cyclecount = 0

print('number of cycles to run set to ', cycles)

pulse = 200

def forward():
    for x in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay_a)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay_b)

    return

def fwdbynum(settime):
    currentcycles = 0
    while (currentcycles < settime):
        forward()
        currentcycles += 1
        print(currentcycles)
        
    return

def fwdbymtime(path, cycles):
    timepassed = 0
    cyclecount = 0
    if (os.path.isfile(path)):
        acesstime = os.path.getmtime(path)
        while (timepassed < 10):
            nacesstime = os.path.getmtime(path)
            if acesstime != nacesstime:
                while (cyclecount < cycles):
                    forward()
                    cyclecount += 1
                    acesstime = nacesstime
                cyclecount = 0
            else :
                print("no change")
            timepassed += 1
            print(timepassed)
            time.sleep(10)
    return

path = "/home/pi/mango/bitProject/test1.txt"

a = int(input())
fwdbynum(a)
print("bynum done")
fwdbymtime(path, 10)

