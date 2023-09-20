# -*- coding: utf-8 -*-

import pickle
import struct
import time
from threading import Thread
import cv2
import socket
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import pyzbar.pyzbar as pyzbar
address = ('127.0.0.1', 6667)


class Ui_check2(object):
    def setupUi(self, check):
        check.setObjectName("check")
        check.resize(1550, 800)
        self.label = QtWidgets.QLabel(check)
        self.label.setGeometry(QtCore.QRect(10, 10, 1000, 700))
        self.label.setText("")
        self.label.setObjectName("camera")

        self.textEdit = QtWidgets.QTextEdit(check)
        self.textEdit.setGeometry(QtCore.QRect(1100, 300, 400, 350))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)

        self.calendarWidget = QtWidgets.QCalendarWidget(check)
        self.calendarWidget.setGeometry(QtCore.QRect(1100, 10, 400, 250))
        self.calendarWidget.setObjectName("calendarWidget")

        self.opencam = QtWidgets.QPushButton(check)
        self.opencam.setGeometry(QtCore.QRect(1100, 700, 100, 30))
        self.opencam.setObjectName("pushButton")
        self.opencam.clicked.connect(self.open)

        self.quit = QtWidgets.QPushButton(check)
        self.quit.setGeometry(QtCore.QRect(1400, 700, 100, 30))
        self.quit.setObjectName("quit")
        self.quit.clicked.connect(self.close)
        self.flag = 0
        self.flag2 = 0
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.qr_detector = cv2.QRCodeDetector()

        self.retranslateUi(check)
        QtCore.QMetaObject.connectSlotsByName(check)

    def closeEvent(self, event):  # 关闭窗口
        if self.flag:
            self.cap.release()
            self.flag = 0
        self.label.setPixmap(QPixmap(""))
        self.textEdit.setText("")
        self.close

    def open(self):  # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.update_frame)
        self.timer_camera.start(30)
        self.flag = 1

    def update_frame(self):  # 获取图像
        ret, self.image = self.cap.read()
        if not ret:
            return
        self.image = cv2.flip(self.image, 1)
        self.display_image()

    def display_image(self):  # 播放收到的影像
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        face = self.face_cascade.detectMultiScale(self.gray, 1.4, 5)
        res = self.detect_qrcode(self.gray)
        if len(face) > 0:
            for (x, y, w, h) in face:
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                self.gray = self.gray[y:y + h, x:x + w]
                break
            if self.flag2 == 0 and res:
                self.flag2 = 1
                p = Thread(target=self.tran_faces)
                p.start()
        outImage = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(outImage))
        self.label.setScaledContents(True)

    def detect_qrcode(self, gray):
        barcodes = pyzbar.decode(gray)
        for barcode in barcodes:
            # 提取条形码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            return 1
        return 0

    def tran_faces(self):  # 送检
        # 传输数据
        s = socket.socket()
        s.connect(address)
        s.send(b"1")
        data = pickle.dumps(self.gray, protocol=2)
        s.sendall(struct.pack("L", len(data)) + data)
        msg = str(s.recv(100), encoding='utf-8')
        self.textEdit.append(msg)
        s.close()
        time.sleep(2)
        self.flag2 = 0

    def retranslateUi(self, check):
        _translate = QtCore.QCoreApplication.translate
        check.setWindowTitle(_translate("check", "特殊考勤"))
        self.quit.setText(_translate("check", "返回"))
        self.opencam.setText(_translate("check", "打开摄像头"))



