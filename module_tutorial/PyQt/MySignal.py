import sys
from PyQt5.QtCore import *

class CustomSignal(QObject):

    mySignal = pyqtSignal(str)

def printstr(text):
    print(text)

if __name__ == '__main__':

    myObject = CustomSignal()

    myObject.mySignal.connect(printstr)

    myObject.mySignal.emit("カスタムシグナル！")
