import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from check1 import Ui_check1
from check2 import Ui_check2
from main import MainWindow as mm


class MainWindows(QMainWindow, mm):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.setupUi(self)
        self.normal.clicked.connect(self.onClicked1)
        self.outbreak.clicked.connect(self.onClicked2)
        self.quit.clicked.connect(self.onClicked)
        self.ChildDialog1 = ChildWin1()
        self.ChildDialog2 = ChildWin2()

    def onClicked1(self):
        # print('打开子窗口！')
        self.ChildDialog1.show()

    def onClicked2(self):
        # print('打开子窗口！')
        self.ChildDialog2.show()

    def onClicked(self):
       sys.exit()


class ChildWin1(QMainWindow, Ui_check1):
    def __init__(self):
        super(ChildWin1, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)


class ChildWin2(QMainWindow, Ui_check2):
    def __init__(self):
        super(ChildWin2, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindows()
    ChildWindow1 = ChildWin1()
    ChildWindow2 = ChildWin2()
    MainWindow.show()
    sys.exit(app.exec_())
