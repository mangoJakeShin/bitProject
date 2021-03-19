import os, sys
from multiprocessing import Process
import subprocess
import time
import psutil
from socket import *
import threading
import RPi.GPIO as GPIO
import VL53L0X
import sys
import argparse
from time import sleep
import signal

pulse = 200

class SocketInfo():
    HOST = "192.168.1.133"
    PORT = 8080
    BUFSIZE = 4
    ADDR = (HOST, PORT)

def mv_left():
    GPIO.output(x_DIR, GPIO.LOW)
    for x in range(pulse):
        GPIO.output(x_PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(x_PUL, GPIO.LOW)
        sleep(delay_L)

    #     print("cur_x : {}".format(cur_x))
    

def mv_right():
    GPIO.output(x_DIR, GPIO.HIGH)
    for y in range(pulse):
        GPIO.output(x_PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(x_PUL, GPIO.LOW)
        sleep(delay_L)

    #     print("cur_x : {}".format(cur_x))
    
def mv_up():
    global cur_y

    GPIO.output(y_DIR, GPIO.LOW)
    GPIO.output(y_ENA, GPIO.HIGH)

    for x in range(pulse):
        GPIO.output(y_PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(y_PUL, GPIO.LOW)
        sleep(delay_L)
    cur_y += 1
    return

def mv_down():
    global cur_y

    GPIO.output(y_DIR, GPIO.HIGH)
    for y in range(pulse):
        GPIO.output(y_PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(y_PUL, GPIO.LOW)
        sleep(delay_L)
    cur_y -= 1
    return

def movePosX(arg, tof):
    global check_x_ok
    print("into moveposx")
    targetPos = int(arg)
    # print("targetPos=",targetPos)

    # Init StopFlag
    contFlag = True

    # get from ToF (distance value)
#     tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
    ToFValue = tof.get_distance() - 30

    print("ToFValue=", ToFValue)

    # set limit
    global x_thr
    x_thr = threading.currentThread()
    
    
    while getattr(x_thr, "do_run", True):
        print("into getattr")
        
        while (ToFValue >= 900) or (ToFValue <= 20):
            if ToFValue > 900:
                mv_left()
            elif (ToFValue <= 20):
                mv_right()
            ToFValue = tof.get_distance() - 30
        while ((ToFValue < 900) and (ToFValue > 20) and check_x_ok):  # while 1
            print("into move_x and state")
            while contFlag:  # while 2
                print("into contFlag")
                # get from ToF (update)
                ToFValue = tof.get_distance() - 30
                #             print (ToFValue, "mm")

                if (ToFValue != targetPos):

                    distance = ToFValue - targetPos

                    if (-2 <= distance <= 2):
                        print("x_move done")
                        return

                    elif (distance > 0):
                        mv_left()
                        print("left")

                    elif (distance < 0):
                        mv_right()
                        print("right")
                # while 2 Exit condition
                else:
                    contFlag = False
                    return
            # while 1 Exit condition
            if (contFlag == False):
                return

#     tof.stop_ranging()
    
    print('Cycling C1ompleted')
    return
    #

def movePosY(arg):
    global cur_y
    global y_thr
    global check_y_ok
    readPos()
    cycles = int(arg)
    y_thr = threading.currentThread()
    
    while ((cur_y > 430) or (cur_y < 10)):
        
        if (cur_y >= 420):
            mv_down()
            sleep(3)
        elif (cur_y <= 10):
            mv_up()
            sleep(3)
    while (cur_y <= 430 and cur_y >= 10 and check_y_ok):
#             check_ok = getattr(y_thr, "do_run", True)
        
        if cur_y == cycles:
            cur_y = str(cur_y)
            pos_close()
            return
        elif cur_y < cycles:
            mv_up()
            print("UP {}".format(cur_y))

        elif cur_y > cycles:
            mv_down()
            print("DOWN {}".format(cur_y))
                
    posInfo = open(postxt, 'w')
    cur_y = str(cur_y)
    pos_close()
    return

def move_y_all():
    movePosY(80)
    print("sleep")
    sleep(1)
    print("sleep wake")
    movePosY(300)
    sleep(1)
    movePosY(420)

def move_x_all():
    global tof
    movePosX(400,tof)

def move_all():
    global thread_x
    global thread_y
    global check_y_ok
    global check_x_ok
    check_x_ok = True
    check_y_ok = True
    thread_x = threading.Thread(target= move_x_all)
    thread_y = threading.Thread(target= move_y_all)
    thread_x.start()
    thread_x.join()
    print("x_start")
    thread_y.start()
    print("y_start")
    
def pos_close():
    global cur_y

    posInfo = open(postxt, 'w')
    cur_y = str(cur_y)

    posInfo.write(cur_y)
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


def handler(signum, f):
    global stopFlag

    print(signum)
    stopFlag = True
    pos_close()
    print("end safeley")
    GPIO.cleanup()
    sys.exit()

# def init_y(arg):
#     os.system("python distance_fy.py -m {}".format(arg))


# def move_init(fx, fy):
#     move_x(fx)
#     init_y(fy)

def kill_move():
    global x_thr
    global y_thr
    global mv_flag
    global check_y_ok
    global check_x_ok

    print("kill_move")
    check_x_ok = False
    check_y_ok = False
    mv_flag = False


# def kill_move():
#     global pid_x
#     global pid_y
#     subprocess.Popen.kill(pid_x)
#     subprocess.Popen.kill(pid_y)


# def move_all():
#     global pid_x
#     global pid_y
#     pid_x = subprocess.Popen(args=[sys.executable, "python3 distance_fx.py -m 400"], shell=True)
#     pid_y = subprocess.Popen(args=[sys.executable, "python3 distance_fy.py"], shell=True)


if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler)

    y_PUL = 26  # Stepper Drive Pulses
    y_DIR = 20  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    y_ENA = 21  # Controller Enable Bit (High to Enable / LOW to Disable).

    x_PUL = 27  # Stepper Drive Pulses
    x_DIR = 18  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    x_ENA = 17  # Controller Enable Bit (High to Enable / LOW to Disable).

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(x_PUL, GPIO.OUT)
    GPIO.setup(x_DIR, GPIO.OUT)
    GPIO.setup(x_ENA, GPIO.OUT)
    GPIO.setup(y_PUL, GPIO.OUT)
    GPIO.setup(y_DIR, GPIO.OUT)
    GPIO.setup(y_ENA, GPIO.OUT)
    GPIO.output(x_ENA, GPIO.HIGH)
    GPIO.output(y_ENA, GPIO.HIGH)

    cyclecount = 0
    global tof
    tof = VL53L0X.VL53L0X(address=0x29)
    tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
    
    global ToFValue
    ToFValue = tof.get_distance() - 30
    pulse = 200  # This is the duration of the motor spinning. used for forward direction
    delay_org = 0.0005
    delay_H = delay_org  # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
    delay_L = delay_H / 2



    postxt = "./pos/y_pos.txt"
    posLines = ["0"]
    global mv_flag
    global cur_y
    readPos()
    global check_y_ok
    global check_x_ok
    
    # global TofValue

    
    ToFValue = tof.get_distance() - 30
    if not os.path.isfile(postxt):
        posInfo = open(postxt, 'w')
        posInfo.writelines(posLines)
        posInfo.close()
    
    
    rasp_socket = socket(AF_INET, SOCK_STREAM)
    rasp_socket.connect(SocketInfo.ADDR)

    #     to_server = int(1)
    #     rasp_msg = to_server.to_bytes(4, byteorder="little")
    #     rasp_sent = rasp_socket.send(rasp_msg)
    mv_flag = False
#     check_x_ok = True
#     check_y_ok = True
    while (1):
        check_y_ok = True
        check_x_ok = True      
        global proc_x
        global proc_y
        ToFValue = tof.get_distance() - 30
        mv_command = rasp_socket.recv(SocketInfo.BUFSIZE, MSG_WAITALL)
        
        print(int.from_bytes(mv_command, byteorder='little'))
#         mv_command = input()
#         new_command = int(mv_command)
        
#         print(mv_command)
#         print(type(mv_command))
        


        if (mv_command):
            new_command = int.from_bytes(mv_command, byteorder='little')
            print("new cmd:", new_command)
            #             new_command = int(mv_command)

            if new_command == 1:  # move all
                if mv_flag == True:
                    kill_move()
                move_all()
                mv_flag = True

            elif new_command == 2:  # stop
                if mv_flag == True:
                    kill_move()                   
                else:
                    continue
            elif new_command == 3:  # left
                if mv_flag == True:
                    kill_move()
                    
                movePosX(ToFValue - 5, tof)
            elif new_command == 4:  # right
                if mv_flag == True:
                    kill_move()
                movePosX(ToFValue + 5, tof)
                
            elif new_command == 5:  # up
                if mv_flag == True:
                    kill_move()
                readPos()
                movePosY(cur_y + 5)
                
            elif new_command == 6:  # down
                if mv_flag == True:
                    kill_move()
                readPos()
                movePosY(cur_y - 5)
                
            elif new_command == 7:
                for i in range(0,5):
                    mv_left()
                    
            elif new_command == 8:
                for i in range(0,5):
                    mv_right()
                    
            elif new_command == 9:
                move_x_all()
                
            elif new_command == 0:
                break
# print(('print : ', sys.argv[0]))
# print(('X pos : ', sys.argv[1]))
# print(('Y pos : ', sys.argv[2]))
# print(sys.argv)
#