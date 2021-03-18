from time import sleep
import RPi.GPIO as GPIO
import VL53L0X
import sys
import argparse


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
    global TofValue
    ToFValue = tof.get_distance() - 30

    print("ToFValue=",ToFValue)

    # set limit
    while (ToFValue >= 900) or (ToFValue <= 20):
        if ToFValue > 900:
            mv_left()
        elif (ToFValue <= 20):
            mv_right()
        ToFValue = tof.get_distance() - 30    
    while ((ToFValue < 900) and (ToFValue > 20)): #while 1
        
        while True: #while 2
            # get from ToF (update)
            ToFValue = tof.get_distance() - 30
#             print (ToFValue, "mm")
            
            if (ToFValue != targetPos):
                
                distance = ToFValue - targetPos

                if (-2 <= distance <=2):
                    break

                elif (distance > 0):
                    mv_left()
                
                elif (distance < 0):
                    mv_right()
                
            #while 2 Exit condition 
            else:
                stopFlag=True
                break
        #while 1 Exit condition         
        if(stopFlag==True):
            break
        
    tof.stop_ranging()

    print('Cycling Completed')
    #

def test():
    while True:

        dist = tof.get_distance()
        
        print("distance={}".format(dist))
        sleep(1)
        

if __name__ == '__main__':
    global TofValue
    PUL = 27  # Stepper Drive Pulses
    DIR = 18  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    ENA = 17  # Controller Enable Bit (High to Enable / LOW to Disable).

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    
    GPIO.output(ENA, GPIO.HIGH)

    tof = VL53L0X.VL53L0X(address = 0x29)
    tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
    
    pulse = 200# This is the duration of the motor spinning. used for forward direction
    delay_org = 0.0005

    delay_H = delay_org # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
    delay_L = delay_H/2
    
    distance = tof.get_distance()
#     test()
#     print(distance)
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', required = False, default = 0)
    parser.add_argument('-l', required = False, default = 0)
    parser.add_argument('-r', required = False, default = 0)
    args = parser.parse_args()
    if args.m == 0:
        movePosX(400)
    elif args.m != 0:
        movePosX(args.m)
    elif args.l != 0:
        movePosX(TofValue -7)
    elif args.r != 0:
        movePosX(TofValue + 7)
    
#usage : python distance_fx.py "int(position you want to place)"
    
