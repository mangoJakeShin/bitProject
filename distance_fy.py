from time import sleep
import RPi.GPIO as GPIO
import os
import sys
import argparse
import signal

postxt = "./pos/y_pos.txt"
posLines = ["0"]
global cur_y

if not os.path.isfile(postxt):
    posInfo = open(postxt, 'w')
    posInfo.writelines(posLines)
    posInfo.close()
    
def readPos():
    
    global cur_y
    
    posInfo = open(postxt, 'r')
    
    for row in posInfo:
        posLines = row
        
    endpos = posLines.split(" ")
    
    cur_y = int(endpos[0])
    print("init cur_y : ", cur_y)
    posInfo.close()

def pos_close():
    global cur_y
    
    
    posInfo = open(postxt, 'w')
    cur_y = str(cur_y)

    posInfo.write(cur_y)
    posInfo.close()
        
def mv_up():
    
    global cur_y
    
    GPIO.output(DIR, GPIO.LOW)
    GPIO.output(ENA, GPIO.HIGH)
    
    for x in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)
    cur_y += 1
    return

def mv_down():
    
    global cur_y
    
    GPIO.output(DIR, GPIO.HIGH)
    for y in range(pulse):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay_L)
    cur_y -= 1
    return

def movePosY(arg):
    global cur_y
    global stopFlag
    
    readPos()
    cycles = int(arg)
    stopFlag = False
    while(stopFlag == False):
        while((cur_y>430) or (cur_y<10)):
            if (cur_y >= 420):
                mv_down()
                sleep(3)
            elif (cur_y <= 10):
                mv_up()
                sleep(3)
        while(cur_y < 430 and cur_y >= 10 and stopFlag == False):
            if cur_y == cycles:
                break
            elif cur_y < cycles:
                mv_up()
                print("UP {}".format(cur_y))    
        
            elif cur_y > cycles:
                mv_down()
                print("DOWN {}".format(cur_y))
    posInfo = open(postxt, 'w')
    cur_y = str(cur_y)
    pos_close()
    
def move_all():
    
    movePosY(80)
    sleep(10)
    movePosY(300)
    sleep(10)
    movePosY(420)

def handler(signum, f):
    global stopFlag
    
    print(signum)
    stopFlag = True
    pos_close()
    print("end safeley")
    GPIO.cleanup()
    sys.exit()
    
    
# readPos()
# move_all()
# pos_close()
if __name__ == '__main__':
    
    signal.signal(signal.SIGINT, handler)
    
    PUL = 26  # Stepper Drive Pulses
    DIR = 20  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    ENA = 21  # Controller Enable Bit (High to Enable / LOW to Disable).

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    
    GPIO.output(ENA, GPIO.HIGH)

    pulse = 200# This is the duration of the motor spinning. used for forward direction
    delay_org = 0.0005

    delay_H = delay_org # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
    delay_L = delay_H/2

    cyclecount = 0 # This is the iteration of cycles to be run once program is started.
#     
#     print("cur_y: ", cur_y)
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', required = False, default = 0)
    parser.add_argument('-u', required = False, default = 0)
    parser.add_argument('-d', required = False, default = 0)
    args = parser.parse_args()
    
    try:
        if args.m == 0:
            move_all()
        elif (args.m !=0):
            target_y = int(args.m)
            movePosY(target_y)
        elif (args.u != 0) or (args.d != 0):
            if args.u != 0:
                targ_y = cur_y +5
            elif args.d != 0:
                targ_y = cury - 5
            movePosY(targ_y)
                
            
    except :
        pos_close()
        print("end safeley")
        GPIO.cleanup()
        
            
        
    print('Cycling Completed')
#usage : python distance_fy.py -m "int(position you want to place)"