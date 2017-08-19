#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
from PyQt5.QtWidgets import *

class SampleWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Sample Window")
        self.setGeometry(300, 300, 200, 150)
        self.setMinimumHeight(100)
        self.setMinimumWidth(250)
        self.setMaximumHeight(100)
        self.setMaximumWidth(250)

if __name__ == '__main__':

        myApp = QApplication(sys.argv)
        myWindow = SampleWindow()
        myWindow.show()
        myApp.exec_()
        sys.exit(0)
