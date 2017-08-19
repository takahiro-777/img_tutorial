import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *

class ColorDialog(QWidget):

    def __init__(self):
        super(ColorDialog, self).__init__(parent=None)
        thisColor = QColor(0, 0, 0)

        self.ColorButton = QPushButton('Select Color', self)
        self.ColorButton.move(27, 15)

        #Qpainterを使う方法もあるが、ここではbackground-colorを設定することで色を変えてみる
        self.myFrame = QFrame(self)
        self.myFrame.setStyleSheet("QWidget { background-color: %s }" % thisColor.name())
        self.myFrame.setGeometry(75, 50, 25, 25)

        self.ColorButton.clicked.connect(self.showDialog)

        self.setGeometry(200, 100, 175, 100)
        self.setWindowTitle('Color Dialog')

        self.show()

    def showDialog(self):
        #ダイアログを表示する
        getcolor = QColorDialog.getColor()

        if getcolor.isValid():
            self.myFrame.setStyleSheet("QWidget { background-color: %s }" % getcolor.name())

if __name__ =='__main__':
        App = QApplication(sys.argv)
        dialog = ColorDialog()
        dialog.show()
        App.exec_()
        sys.exit()
