# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register1.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os.path
from threading import Thread
from PyQt5 import QtCore, QtWidgets
import cv2
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox, QWidget
from train import train
import pymysql

address = ('127.0.0.1', 6666)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Ntss2000')
cursor = db.cursor()


class Ui_register(object):
    def setupUi(self, register):
        register.setObjectName("register")
        register.resize(1600, 800)
        self.label = QtWidgets.QLabel(register)
        self.label.setGeometry(QtCore.QRect(10, 10, 1200, 700))
        self.label.setText("")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(register)
        self.label_2.setGeometry(QtCore.QRect(1350, 50, 60, 30))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(register)
        self.label_3.setGeometry(QtCore.QRect(1350, 130, 60, 30))
        self.label_3.setObjectName("label_3")

        self.name = QtWidgets.QLineEdit(register)
        self.name.setGeometry(QtCore.QRect(1400, 50, 150, 30))
        self.name.setObjectName("name")
        reg = QRegExp("[\u4e00-\u9fa5]+$")  # 只允许输入汉字
        validator = QRegExpValidator(reg)
        self.name.setValidator(validator)

        self.number = QtWidgets.QLineEdit(register)
        self.number.setGeometry(QtCore.QRect(1400, 130, 150, 30))
        self.number.setObjectName("number")
        self.number.setMaxLength(6)
        int_validator = QIntValidator()
        self.number.setValidator(int_validator)

        self.open = QtWidgets.QPushButton(register)
        self.open.setGeometry(QtCore.QRect(1390, 270, 100, 30))
        self.open.setObjectName("pushButton")
        self.open.clicked.connect(self.opencap)

        self.collect = QtWidgets.QPushButton(register)
        self.collect.setGeometry(QtCore.QRect(1390, 320, 100, 30))
        self.collect.setObjectName("pushButton")
        self.collect.clicked.connect(lambda: self.collectinfo())

        self.train = QtWidgets.QPushButton(register)
        self.train.setGeometry(QtCore.QRect(1390, 370, 100, 30))
        self.train.setObjectName("pushButton")
        self.train.clicked.connect(lambda: self.video_demo_train())

        self.quit = QtWidgets.QPushButton(register)
        self.quit.setGeometry(QtCore.QRect(1390, 420, 100, 30))
        self.quit.setObjectName("quit")
        self.quit.clicked.connect(self.close)
        self.flag = 0

        self.retranslateUi(register)
        QtCore.QMetaObject.connectSlotsByName(register)

    def closeEvent(self, event):  # 关闭窗口
        if self.flag:
            self.cap.release()
            self.flag = 0
        self.label.setPixmap(QPixmap(""))
        self.close

    def opencap(self):  # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.update_frame)
        self.timer_camera.start(30)
        self.flag = 1
        self.update_frame()

    def update_frame(self):
        ret, self.image = self.cap.read()
        if not ret:
            return
        self.image = cv2.flip(self.image, 1)
        self.display_image()

    def collectinfo(self):
        if not self.flag:
            self.msgbox("请先打开摄像头！")
            return
        if not self.name.text() or not self.number.text():
            self.msgbox("工号和姓名不能为空！")
            return
        if len(self.number.text()) != 6:
            self.msgbox("请输入六位工号！")
            return

        face_name = self.name.text()
        face_ID = self.number.text()
        sql = "select * from employee.today where number = '{}'".format(face_ID)
        cursor.execute(sql)
        res = cursor.fetchall()
        if not res:
            if not os.path.exists('./train/%s' % str(face_ID)):
                os.mkdir('./train/%s' % str(face_ID))
            sql = "INSERT INTO employee.today (number, name) VALUES ('{}', '{}')".format(face_ID, face_name)
            cursor.execute(sql)
            db.commit()
            p = Thread(target=self.video_demo_collect)
            p.start()
            p.join()
            self.msgbox("录入成功！")
        else:
            w = QWidget()
            reply = QMessageBox.question(w, '提示', '已存在相同工号，确定重新录入？', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                sql = "update employee.today set name='{}' where number='{}'".format(face_name, face_ID)
                cursor.execute(sql)
                db.commit()
                if not os.path.exists('./train/%s' % str(face_ID)):
                    os.mkdir('./train/%s' % str(face_ID))
                p = Thread(target=self.video_demo_collect)
                p.start()
                p.join()
                self.msgbox("录入成功！")
            else:
                return

    def video_demo_collect(self):
        face_ID = self.number.text()
        count = 1
        while (True):
            ref, frame = self.cap.read()
            if not ref:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.2, 5)
            if count > 50:
                break
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                f = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
                # 保存图像
                cv2.imwrite('./train/%s/%s.jpg' % (str(face_ID), str(count)), f)
                count += 1
                break

    def video_demo_train(self):
        p = Thread(target=train)
        p.start()
        p.join()
        self.msgbox("训练完成！")

    def display_image(self):  # 播放收到的影像
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:  # 标准化显示图片格式
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(outImage))
        self.label.setScaledContents(True)

    def msgbox(self, txt):  # 提示框
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(txt)
        msg.setWindowTitle("提示")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def retranslateUi(self, register1):
        _translate = QtCore.QCoreApplication.translate
        register1.setWindowTitle(_translate("register", "录入信息"))
        self.label_2.setText(_translate("register", "姓名"))
        self.label_3.setText(_translate("register", "工号"))
        self.open.setText(_translate("register", "打开摄像头"))
        self.collect.setText(_translate("register", "录入信息"))
        self.train.setText(_translate("register", "训练模型"))
        self.quit.setText(_translate("register", "返回"))
