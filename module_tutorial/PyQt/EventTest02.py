import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

class Test(QWidget):
    def __init__(self,parent=None):
        super(Test, self).__init__(parent)
        self.label = QLabel(self)
        self.label.setText('テストボックス')

        #http://doc.qt.io/qt-5/qt.html
        #上記のページに他の設定もあります
        self.label.setAlignment(Qt.AlignCenter)

        #http://doc.qt.io/qt-5/qframe.html
        #上記のページに他の設定もあります
        self.label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.label.setLineWidth(2)

        #マウストラッキングが有効になっている場合、ウィジェットはボタンを押さない場合でも、マウス移動イベントを受け取ります。
        self.label.setMouseTracking(True)

        self.label.installEventFilter(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress and object is self.label:
            pos = event.pos()
            print('MouseButtonPress: (%d, %d)' % (pos.x(), pos.y()))
        return QWidget.eventFilter(self, object, event)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    window.resize(300, 150)
    sys.exit(app.exec_())
    
