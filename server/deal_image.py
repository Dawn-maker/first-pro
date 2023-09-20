# -*- coding: utf-8 -*-
import datetime
import struct
import pickle
import cv2
import numpy as np
import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Ntss2000')
cursor = db.cursor()
now = datetime.datetime.now()
start_time = datetime.datetime(now.year, now.month, now.day, 9, 0, 0)


def deal_image(sock, fn, model):
    data = b""
    msg = "未知人员"

    payload_size = struct.calcsize("L")  # 接收灰度图
    while len(data) < payload_size:
        data += sock.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += sock.recv(4096)
    frame_data = data[:msg_size]
    gray = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

    resized_img = cv2.resize(gray, (100, 100))  # 人脸识别
    normalized_img = resized_img / 255.0
    reshaped_img = np.reshape(normalized_img, (1, 100, 100, 1))
    result = model.predict(reshaped_img)
    print(np.max(result))
    print(fn[np.argmax(result)])

    if np.max(result) < 0.85:  # 准确率不够，不能认定为是同一个人
        sock.send(bytes(msg.encode()))
        return

    sql = "select name from employee.today where number = '{}'".format(fn[np.argmax(result)])
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        nowp = datetime.datetime.now()
        if nowp > start_time:
            attend = '迟到'
        else:
            attend = '已到'
        msg = res[0][0] + '签到成功'
        sql = "update employee.today set time = '{}', attend = '{}' where number = '{}'".format(
            datetime.datetime.now(),
            attend,
            fn[np.argmax(result)]
        )
        cursor.execute(sql)
        db.commit()

    sock.send(bytes(msg.encode()))
    sock.close()
