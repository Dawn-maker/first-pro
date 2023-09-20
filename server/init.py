import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from kaoqin import Ui_Dialog
from main import Ui_MainWindow as mm
from register import Ui_register


class MainWindows(QMainWindow, mm):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.setupUi(self)
        self.kqmsg.clicked.connect(self.onClicked1)
        self.addmsg.clicked.connect(self.onClicked2)
        self.quit.clicked.connect(self.onClicked3)
        self.ChildDialog1 = ChildWin1()
        self.ChildDialog2 = ChildWin2()

    def onClicked1(self):
        self.ChildDialog1.show()

    def onClicked2(self):
        self.ChildDialog2.show()

    def onClicked3(self):
       sys.exit()


class ChildWin1(QMainWindow, Ui_Dialog):
    def __init__(self):
        super(ChildWin1, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)


class ChildWin2(QMainWindow, Ui_register):
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
