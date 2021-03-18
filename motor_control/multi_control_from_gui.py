import os, sys
from socket import *
import threading
import RPi.GPIO as GPIO
import VL53L0X
from time import sleep
import signal

global Debug

Debug = False

pulse = 200


class SocketInfo():
    HOST = "127.0.0.1"
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



def mv_right():
    GPIO.output(x_DIR, GPIO.HIGH)
    for y in range(pulse):
        GPIO.output(x_PUL, GPIO.HIGH)
        sleep(delay_H)
        GPIO.output(x_PUL, GPIO.LOW)
        sleep(delay_L)


def mv_up():
    global cur_y
    GPIO.output(y_DIR, GPIO.LOW)

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
    targetPos = int(arg)

    ToFValue = tof.get_distance() - 30

    print("ToFValue=", ToFValue)

    # if the machine is out of rail, automatically comes back into range
    while (ToFValue >= 900) or (ToFValue <= 20):
        if ToFValue > 900:
            mv_left()
        elif (ToFValue <= 20):
            mv_right()
        ToFValue = tof.get_distance() - 30

    # sets end of range, and Flag for emergency stop
    while ((ToFValue < 900) and (ToFValue > 20) and check_x_ok):  # while 1
        # get from ToF (update)
        ToFValue = tof.get_distance() - 30
        #             print (ToFValue, "mm")

        if (ToFValue != targetPos):
            # from the ToF sensor, we can calculate the distance between destination and the starting point
            distance = ToFValue - targetPos

            # if machine arrives the destination, returns
            if (-2 <= distance <= 2):
                return
            # if distance is bigger than 0, the machine moves left
            elif (distance > 0):
                mv_left()
                print("left")

            # if distance is smaller than 0, the machine moves left
            elif (distance < 0):
                mv_right()
                print("right")

    #     tof.stop_ranging()

    print('Cycling C1ompleted')
    return
    #


def movePosY(cycles):
    # moving y_axis machine works with similar logic with moving x_axis machine, but the difference is
    # y_axis uses cur_y argument, which let us know where the machine is currently located

    global cur_y
    global y_thr
    global check_y_ok
    readPos()

    while ((cur_y > 430) or (cur_y < 10)):

        if (cur_y >= 420):
            mv_down()
            sleep(3)
        elif (cur_y <= 10):
            mv_up()
            sleep(3)

    while (cur_y <= 430 and cur_y >= 10 and check_y_ok):
        if cur_y == cycles:
            cur_y = str(cur_y)
            pos_close()
            return
        elif cur_y < cycles:
            mv_up()

        elif cur_y > cycles:
            mv_down()

    pos_close()
    return


def move_y_all():
    # when called, it moves y_axis machine to the designated point, which is 80, 300, 420
    # and for depth camera to take a picture, it stops for a while

    movePosY(80)
    sleep(1)
    movePosY(300)
    sleep(1)
    movePosY(420)


def move_x_all():
    # when called, it moves x_axis machine to the center point
    global tof
    movePosX(400, tof)


def move_all():
    # in order to move x and y axis machine at same time, we tried to use multi-thread
    # however, it continuously raised an error to the motor, so we decided to wait until x_axis movement is done
    global thread_x
    global thread_y
    global check_y_ok
    global check_x_ok
    check_x_ok = True
    check_y_ok = True
    thread_x = threading.Thread(target=move_x_all)
    thread_y = threading.Thread(target=move_y_all)
    thread_x.start()
    thread_x.join()
    print("x_start")
    thread_y.start()
    print("y_start")


def pos_close():
    # pos_close saves the current y position
    global cur_y

    posInfo = open(postxt, 'w')
    cur_y = str(cur_y)

    posInfo.write(cur_y)
    posInfo.close()


def readPos():

    # readpos gets the last point of y_axis machine
    global cur_y

    posInfo = open(postxt, 'r')

    for row in posInfo:
        posLines = row

    endpos = posLines.split(" ")

    cur_y = int(endpos[0])
    posInfo.close()


def handler(signum, f):
    # this is to save the cur_y in the text file whenever the process is stopped
    global stopFlag
    stopFlag = True
    pos_close()

    print("safe end")
    GPIO.cleanup()
    sys.exit()

def kill_move():
    global x_thr
    global y_thr
    global mv_flag
    global check_y_ok
    global check_x_ok

    # when the False flag is checked in movePosX and movePosY, they stop immidiately
    check_x_ok = False
    check_y_ok = False
    mv_flag = False


if __name__ == '__main__':
    global DEBUG
    signal.signal(signal.SIGINT, handler)

    y_PUL = 26
    y_DIR = 20
    y_ENA = 21

    x_PUL = 27
    x_DIR = 18
    x_ENA = 17

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(x_PUL, GPIO.OUT)
    GPIO.setup(x_DIR, GPIO.OUT)
    GPIO.setup(x_ENA, GPIO.OUT)
    GPIO.setup(y_PUL, GPIO.OUT)
    GPIO.setup(y_DIR, GPIO.OUT)
    GPIO.setup(y_ENA, GPIO.OUT)
    GPIO.output(x_ENA, GPIO.HIGH)
    GPIO.output(y_ENA, GPIO.HIGH)

    global tof
    tof = VL53L0X.VL53L0X(address=0x29)
    tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)

    global ToFValue
    ToFValue = tof.get_distance() - 30
    pulse = 200  # This is the duration of the motor spinning. used for forward direction
    delay_org = 0.0005
    delay_H = delay_org  # This is actually a delay between PUL pulses - effectively sets the motor rotation speed.
    delay_L = delay_H / 2

    # since we could not put a sensor on y axis, we needed a method to manage a current y point
    # to save current y axis point, we used a text file and it is managed by readpos and pos_close method
    postxt = "./pos/y_pos.txt"
    posLines = ["0"]
    global mv_flag
    global cur_y
    readPos()
    global check_y_ok
    global check_x_ok

    if not os.path.isfile(postxt):
        posInfo = open(postxt, 'w')
        posInfo.writelines(posLines)
        posInfo.close()

    rasp_socket = socket(AF_INET, SOCK_STREAM)
    rasp_socket.connect(SocketInfo.ADDR)

    mv_flag = False
    #     check_x_ok = True
    #     check_y_ok = True
    while (1):
        check_y_ok = True
        check_x_ok = True
        global proc_x
        global proc_y
        ToFValue = tof.get_distance() - 30
        if DEBUG:
            mv_command = input()
            new_command = int(mv_command)
        else:
            # even though our GUI is designed in python, our socket passes through a C based server
            # thus, we needed to send packet that is byte-typed, and decode it, in order to prevent packet loss
            mv_command = rasp_socket.recv(SocketInfo.BUFSIZE, MSG_WAITALL)
            new_command = int.from_bytes(mv_command, byteorder='little')


        if (mv_command):
            print("new cmd:", new_command)
            #

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
                for i in range(0, 5):
                    mv_left()

            elif new_command == 8:
                for i in range(0, 5):
                    mv_right()

            elif new_command == 9:
                move_x_all()

            elif new_command == 0:
                break

    print("bye bye")