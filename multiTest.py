import os, sys
from multiprocessing import Process
import subprocess
import time
import psutil
from socket import *

class SocketInfo():
    HOST = "192.168.1.133"
    PORT = 8080
    BUFSIZE = 4
    ADDR = (HOST, PORT)
    
# def move_x(fx):
#     global pid_x
#     pid_x = subprocess.Popen(args = [sys.executable, "python distance_fx -m 400.py"])
# #     os.system("python distance_fx.py -m {} &" .format(fx))
    
def move_x_left():
    os.system("python distance_fx.py -l {} &" .format(1))
    
def move_x_right():
    os.system("python distance_fy.py -u {} &" .format(1))

def move_y_up():
    os.system("python distance_fy.py -d {} &" .format(1))
    
def move_y_down():
    os.system("python distance_fx.py -l {} &" .format(1))
    
# def move_y():
#     global pid_y
#     pid_y = subprocess.Popen(args = [sys.executable, "python distamce_fy.py"])
#     time.sleep(20)
    
#     os.system("python distance_fy.py")
    
    
def init_y(arg):
    os.system("python distance_fy.py -m {}".format(arg))
    

def move_init(fx, fy):
    move_x(fx)
    init_y(fy)
    
def kill_move():
    global pid_x
    global pid_y
    subprocess.Popen.kill(pid_x)
    subprocess.Popen.kill(pid_y)

def move_all():
    global pid_x
    global pid_y
    pid_x = subprocess.Popen(args = [sys.executable, "python3 distance_fx.py -m 400"], shell = True)
    pid_y = subprocess.Popen(args = [sys.executable, "python3 distance_fy.py"], shell = True)
    
if __name__ == '__main__':
    
    global mv_flag
    
    rasp_socket = socket(AF_INET, SOCK_STREAM)
    rasp_socket.connect(SocketInfo.ADDR)

#     to_server = int(1)
#     rasp_msg = to_server.to_bytes(4, byteorder="little")
#     rasp_sent = rasp_socket.send(rasp_msg)
    
    while(1):
        global proc_x
        global proc_y
        
        mv_command = rasp_socket.recv(SocketInfo.BUFSIZE, MSG_WAITALL)
        print(mv_command)
        print(type(mv_command))
        if (mv_command):
            new_command = int.from_bytes(mv_command, byteorder = 'little')
            print(new_command)
            print(type(new_command))
#             new_command = int(mv_command)
            mv_flag = False
            
        
            if new_command == 1 : #move all
                if mv_flag == True:
                
                    kill_move()
                move_all()
                
            elif new_command == 2 : #stop
                if mv_flag == True:
                
                    kill_move()
                    mv_flag == False
                else:
                    pass
            elif new_command == 3: #left
                if mv_flag == True:
                    kill_move()
                    mv_flag == False
                move_x_left()
            elif new_command == 4: #right
                if mv_flag == True:
                    kill_move()
                    mv_flag == False
                move_x_right()
            elif new_command == 5: #up
                if mv_flag == True:
                    kill_move()
                    mv_flag == False
                move_y_up()
            elif new_command == 6: #down
                if mv_flag == True:
                    kill_move()
                    mv_flag == False
                move_y_down()
        
# print(('print : ', sys.argv[0]))
# print(('X pos : ', sys.argv[1]))
# print(('Y pos : ', sys.argv[2]))
# print(sys.argv)
#  
 