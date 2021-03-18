from socket import *
from time import sleep, time
import datetime
import RPi.GPIO as GPIO
import os
import time
import VL53L0X
import X_motor as Xm

#GPIO setup for tof sensor
tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
GPIO.setmode(GPIO.BCM)

#check if step motor direction is set correctly
distance = tof.get_distance()
testmove = Xm.mover()

testmove.mv_left(5)
new_distance = tof.get_distance()
if abs(distance - new_distance) > 5:
    if distance > new_distance:
        rasp = Xm.mover()

    elif distance < new_distance:
        rasp = Xm.mover()

class SocketInfo():
    HOST = "127.0.0.1"
    PORT = 80
    BUFSIZE = 7
    ADDR = (HOST, PORT)

#실행 시 지정된 호스트 및 포트로 연결

rasp_socket = socket(AF_INET, SOCK_STREAM)
rasp_socket.connect(SocketInfo.ADDR)

#연결 성공 시 메시지 송신
to_server = int(1)
rasp_msg = to_server.to_bytes(4, byteorder="little")
rasp_sent = rasp_socket.send(rasp_msg)

#연결 후 메시지 수신 대기

mv_command = rasp_socket.recv(SocketInfo.BUFSIZE, MSG_WAITALL)

#메시지 수신 시 디코딩 실행
if (mv_command):
    mv_command = mv_command.decode("UTF-8")

try:
    new_command = int(mv_command)

except:
    print("msg command is not readable")

#check
distance = tof.get_distance()
testmove = Xm.mover()

testmove.mv_left(5)
new_distance = tof.get_distance()


