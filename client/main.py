# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets


class MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.normal = QtWidgets.QPushButton(self.centralwidget)
        self.normal.setGeometry(QtCore.QRect(350, 150, 100, 32))
        self.normal.setObjectName("normal")


        self.outbreak = QtWidgets.QPushButton(self.centralwidget)
        self.outbreak.setGeometry(QtCore.QRect(350, 210, 100, 32))
        self.outbreak.setObjectName("outbreak")

        self.quit = QtWidgets.QPushButton(self.centralwidget)
        self.quit.setGeometry(QtCore.QRect(350, 270, 100, 32))
        self.quit.setObjectName("quit")

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(350, 70, 200, 41))
        self.title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title.setAutoFillBackground(False)
        self.title.setObjectName("title")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.normal.setText(_translate("MainWindow", "一般考勤"))
        self.outbreak.setText(_translate("MainWindow", "特殊考勤"))
        self.quit.setText(_translate("MainWindow", "退出"))
        self.title.setText(_translate("MainWindow", "人脸识别考勤系统"))

