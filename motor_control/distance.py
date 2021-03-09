from time import sleep, time
import datetime 
import RPi.GPIO as GPIO
import os
import time
import VL53L0X

postxt = "./pos/x_pos.txt"
posLines = ["0"]

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
if not os.path.isfile(postxt):
    posInfo = open(postxt, 'w')
    posInfo.writelines(posLines)
    posInfo.close()
    
posInfo = open(postxt, 'r')
for row in posInfo:
    posLines = row
    
endpos = posLines.split(" ")
global cur_x
cur_x = int(endpos[0])
max_x = 390
able_x = 390 - cur_x
posInfo.close()

PUL = 27  # Stepper Drive Pulses
DIR = 18  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 17  # Controller Enable Bit (High to Enable / LOW to Disable).



GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pulse = 200# This is the duration of the motor spinning. used for forward direction
delay_org = 0.0005

delay_H = delay_org # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
delay_L = delay_H/2

#cycles = 50# This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.

def mv_left():
    global cur_x
    
    GPIO.output(DIR, GPIO.LOW)
    GPIO.output(ENA, GPIO.HIGH)
    
    for x in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)
    cur_x -= 1
#     print("cur_x : {}".format(cur_x))
    return


def mv_right():
    global cur_x
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(DIR, GPIO.HIGH)
    for y in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)
    cur_x += 1
#     print("cur_x : {}".format(cur_x))
    return

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
#
if (cur_x >= 390):
    mv_left()
    sleep(5)
elif (cur_x <= 10):
    mv_right()
    sleep(5)
distance = tof.get_distance()
print (distance, "mm")
# print(type(distance))

while ((cur_x < 390) and (cur_x > 10) and (distance < 900) and (distance > 30 )):
    while(distance>400):
        mv_left() #move left, cur_x -
        #mv_right() # move right, cur_x +
        cyclecount += 1
#         if(cur_x < 390):
#             print("motor out of rail")
#         elif(cur_x > 10):
#             print("motor out of rail")
#         elif(distance < 700):
#             print("too close to end")
#         elif(distance > 30):
#             print("too close to start")
        distance = tof.get_distance()
        print (distance, "mm")
        break

tof.stop_ranging()
GPIO.cleanup()
print('Cycling Completed')
#