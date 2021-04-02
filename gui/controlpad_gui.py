from PyQt5 import uic
import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
form_class = uic.loadUiType("controlpad.ui")[0]
from socket import *
import csv

DEBUG = False

class SocketInfo():
    HOST = "127.0.0.1"
    PORT = 80
    BUFSIZE = 7
    ADDR = (HOST, PORT)


class MyApp(QMainWindow,form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.show()

    def initUI(self):
        self.setWindowTitle('control pad')
        self.runAllBtn.clicked.connect(self.sendRunAll)
        self.stopBtn.clicked.connect(self.sendStop)
        self.leftBtn.clicked.connect(self.sendLeft)
        self.rightBtn.clicked.connect(self.sendRight)
        self.upBtn.clicked.connect(self.sendUp)
        self.downBtn.clicked.connect(self.sendDown)
        # self.call_csv()
        self.show()

    def call_csv(self):
        readlines = []
        with open('test.csv', newline='') as info:
            reader = csv.reader(info)
            for row in reader:
                readlines.append(row)
        max = len(readlines)

        for idx in range(1,max):
            obj = readlines[idx][0]
            amount = readlines[idx][1]
            time = readlines[idx][2]
            place = readlines[idx][4]
            self.set_col(idx-1, obj, amount, time, place)


    def set_col(self, row, obj, amount, time, place):
        self.statustable.setItem(row, 0, QTableWidgetItem(obj))
        self.statustable.setItem(row, 1, QTableWidgetItem(amount))
        self.statustable.setItem(row, 2, QTableWidgetItem(time))
        self.statustable.setItem(row, 3, QTableWidgetItem(place))


    def sendRunAll(self):
        to_server = 1
        self.sendMsg(to_server)


    def sendStop(self):
        to_server = 2
        self.sendMsg(to_server)

    def sendLeft(self):
        to_server = 3
        self.sendMsg(to_server)

    def sendRight(self):
        to_server = 4
        self.sendMsg(to_server)

    def sendUp(self):
        to_server = 5
        self.sendMsg(to_server)

    def sendDown(self):
        to_server = 6
        self.sendMsg(to_server)


    def sendMsg(self, msg):
        if (DEBUG):
            print(msg)
        else:
            to_server = int(msg)
            senddata = to_server.to_bytes(4, byteorder="little")
            sent = csock.send(senddata)
            print("Sent : {}".format(to_server))

if __name__ == '__main__':

    if (DEBUG):
        pass

    else:
        print("trying to connect")
        csock = socket(AF_INET, SOCK_STREAM)
        csock.connect(SocketInfo.ADDR)
        command = csock.recv(SocketInfo.BUFSIZE, MSG_WAITALL)
        data = command.decode("UTF-8")
        if (command):
            print("conecction success")
            print("type : {}, data len : {}, data : {}, Contents : {}".format(type(command), len(command), command, data))

            to_server = int(0)
            senddata = to_server.to_bytes(4, byteorder='little')
            sent = csock.send(senddata)
        else:
            print("connection failed")
            exit()

    app = QApplication(sys.argv)
    ex = MyApp()
    if (DEBUG == False):
        csock.close()
        
    sys.exit(app.exec_())
