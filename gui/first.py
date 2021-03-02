from PyQt5 import uic
import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
form_class = uic.loadUiType("first.ui")[0]
from socket import *

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
        self.setWindowTitle('first try')
        self.runAllBtn.clicked.connect(self.sendRunAll())
        self.stopBtn.clicked.connect(self.sendStop())
        self.leftBtn.clicked.connect(self.sendLeft())
        self.rightBtn.clicked.connect(self.sendRight())
        self.upBtn.clicked.connect(self.sendUp())
        self.downBtn.clicked.connect(self.sendDown())
        # self.runTab.currentTabText("runTab")
        self.show()

    def sendRunAll(self):
        to_server = int(1)
        senddata = to_server.to_bytes(4, byteorder = "little")
        sent = csock.send(senddata)
        print("Sent : {}".format(to_server))


    def sendStop(self):
        to_server = int(2)
        senddata = to_server.to_bytes(4, byteorder="little")
        sent = csock.send(senddata)
        print("Sent : {}".format(to_server))

    def sendLeft(self):
        to_server = int(3)
        senddata = to_server.to_bytes(4, byteorder="little")
        sent = csock.send(senddata)
        print("Sent : {}".format(to_server))

    def sendRight(self):
        to_server = int(4)
        senddata = to_server.to_bytes(4, byteorder="little")
        sent = csock.send(senddata)
        print("Sent : {}".format(to_server))

    def sendUp(self):
        to_server = int(5)
        senddata = to_server.to_bytes(4, byteorder="little")
        sent = csock.send(senddata)
        print("Sent : {}".format(to_server))

    def sendDown(self):
        to_server = int(6)
        senddata = to_server.to_bytes(4, byteorder="little")
        sent = csock.send(senddata)
        print("Sent : {}".format(to_server))


if __name__ == '__main__':

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
    sys.exit(app.exec_())
    csock.close()
    exit()