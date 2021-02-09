from PyQt5 import uic
import sys
import cv2
from matplotlib import pyplot as plt
import PyQt5.QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os
import numpy as np
from PIL import Image

form_class = uic.loadUiType("first.ui")[0]


class MyApp(QMainWindow,form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.show()

    def initUI(self):
        self.setWindowTitle('first try')
        # self.runTab.currentTabText("runTab")
        self.show()



if __name__ == '__main__':


    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())