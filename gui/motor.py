import time
import RPi.GPIO as GPIO
import os
import datetime
from socket import *

GPIO.setmode(GPIO.BCM)


print("initialization completed")


cycles = 10
cyclecount = 0

print('number of cycles to run set to ', cycles)

pulse = 200

class SocketInfo():
    HOST = "127.0.0.1"
    PORT = 80
    BUFSIZE = 7
    ADDR = (HOST, PORT)

class pins():
    ENA = 0
    DIR = 0
    PUL = 0
    delay_a = 0.0005
    delay_b = 0.00025

    def setInit(self, PUL, DIR, ENA):
        self.PUL = PUL
        self.DIR = DIR
        self.ENA = ENA
        GPIO.setup(PUL, GPIO.OUT)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(ENA, GPIO.OUT)

    def setBwd(self):
        GPIO.setmode(self.DIR, GPIO.LOW)
    def setFwd(self):
        GPIO.setmode(self.DIR, GPIO.HIGH)

    def forward(self):
        for x in range(pulse):
            GPIO.output(self.PUL, GPIO.HIGH)
            time.sleep(self.delay_a)
            GPIO.output(self.PUL, GPIO.LOW)
            time.sleep(self.delay_b)


    def fwdbysettime(self, settime):
        currentcycles = 0

        while (currentcycles < settime):
            self.forward()
            currentcycles += 1
            print(currentcycles)

        return


    def fwdbymtime(self, path, cycles):
        timepassed = 0
        cyclecount = 0
        if (os.path.isfile(path)):
            acesstime = os.path.getmtime(path)
            while (timepassed < 10):
                nacesstime = os.path.getmtime(path)
                if acesstime != nacesstime:
                    while (cyclecount < cycles):
                        self.forward()
                        cyclecount += 1
                        acesstime = nacesstime
                    cyclecount = 0
                else:
                    print("no change")
                timepassed += 1
                print(timepassed)
                time.sleep(10)
        return

    def backward(self):
        GPIO.setmode(self.DIR, GPIO.LOW)
        for x in range(pulse):
            GPIO.output(self.PUL, GPIO.HIGH)
            time.sleep(self.delay_a)
            GPIO.output(self.PUL, GPIO.LOW)
            time.sleep(self.delay_b)

newpin = pins
newpin.setInit(23,24,25)

csock = socket(AF_INET, SOCK_STREAM)
csock.connect(SocketInfo.ADDR)

while(1):
    command = csock.recv(SocketInfo.BUFSIZE, MSG_WAITALL)
    data = command.decode("UTF-8")
    print(data)

    if (data == 1):
        newpin.setFwd()
        newpin.fwdbysettime(10)
    elif(data == 2):
        newpin.setBwd()
        newpin.fwdbysettime(10)
    else:
        break

# path = "/home/pi/mango/bitProject/test1.txt"
#
# a = int(input())
# fwdbynum(a)
# print("bynum done")
# fwdbymtime(path, 10)