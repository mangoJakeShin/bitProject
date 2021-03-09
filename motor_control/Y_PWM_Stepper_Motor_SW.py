from time import sleep, time
import datetime 
import RPi.GPIO as GPIO


PUL = 26  # Stepper Drive Pulses
DIR = 20  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 21  # Controller Enable Bit (High to Enable / LOW to Disable).


#mode2

#PUL = 19
#DIR = 16
#ENA = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pulse = 200# This is the duration of the motor spinning. used for forward direction
delay_org = 0.0005

delay_H = delay_org # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
delay_L = delay_H/2

cycles = 50# This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.

def forward():
    GPIO.output(DIR, GPIO.LOW)
    GPIO.output(ENA, GPIO.HIGH)
    for x in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)
    return


def reverse():
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(DIR, GPIO.HIGH)
    for y in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)
        
    return

start = time()
timetaken = time()-start
backnforth = 0

# while(backnforth < 3):
#     while cyclecount < cycles:
# 
#         reverse()
#                
#         cyclecount = cyclecount+1
#         print("backward {}".format(cyclecount))
#         
#     sleep(2)
#     while cyclecount > 0 :
#         forward()
#         
#         
#         cyclecount = (cyclecount -1)
#         print("forward{}".format(cyclecount))
#     
#     sleep(2)
#     backnforth += 1
# print(datetime.datetime.fromtimestamp(timetaken))
# print(cyclecount)

while cyclecount <10 :
    #forward()#up
    reverse()
    cyclecount += 1
# #     
GPIO.cleanup()
print('Cycling Completed')
#

