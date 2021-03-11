from time import sleep, time
import datetime 
import RPi.GPIO as GPIO
import os
import time
import VL53L0X
import sys


def mv_left():
    GPIO.output(DIR, GPIO.LOW)
    for x in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)

#     print("cur_x : {}".format(cur_x))
    return


def mv_right():
    GPIO.output(DIR, GPIO.HIGH)
    for y in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)

#     print("cur_x : {}".format(cur_x))
    return

def movePosX(arg):
    
    targetPos = int(arg)
    #print("targetPos=",targetPos)
    
    # Init StopFlag
    stopFlag = False

    # get from ToF (distance value)
    ToFValue = tof.get_distance() - 45

    print("ToFValue=",ToFValue)

    # set limit
    while ((ToFValue < 900) and (ToFValue > 0)):
        
        while True:
            # get from ToF (update)
            ToFValue = tof.get_distance() - 45
            print (ToFValue, "mm")
            
            
            if (ToFValue != targetPos):
                
                distance = ToFValue - targetPos

                if (-2 <= distance <=2):
                    break

                elif (distance > 0):
                    mv_left()
                
                elif (distance < 0):
                    mv_right()
                

            
            # Exit condition
            else:
                stopFlag=True
                break
                
        if(stopFlag==True):
            break
            
        
            

    tof.stop_ranging()

    print('Cycling Completed')
    #


if __name__ == '__main__':

    GPIO.cleanup()

    PUL = 27  # Stepper Drive Pulses
    DIR = 18  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    ENA = 17  # Controller Enable Bit (High to Enable / LOW to Disable).

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    
    GPIO.output(ENA, GPIO.HIGH)

    tof = VL53L0X.VL53L0X()
    tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)



    pulse = 200# This is the duration of the motor spinning. used for forward direction
    delay_org = 0.0005

    delay_H = delay_org # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
    delay_L = delay_H/2
    movePosX(700)

#     movePosX(sys.argv[1])
