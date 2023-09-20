# -*- coding: utf-8 -*-
import os
import socket
from deal_image import deal_image
from keras.models import load_model

fn = os.listdir('./train')
fn.remove('.DS_Store')
fn.sort()
model = load_model('model.h5')
print(fn)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 6667))
s.listen(1000)
print("Wait for Connection...")
while True:
        sock, addr = s.accept()  # addr是一个元组(ip,port)
        num = sock.recv(1)
        if num == b"1":
            deal_image(sock, fn, model)
        elif num == b"2":
            model = load_model('model.h5')
            fn = os.listdir('./train')
            fn.remove('.DS_Store')
            fn.sort()
        else:
            sock.send(b"uninvaild command")
            sock.close()
