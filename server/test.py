# import cv2
# from keras.models import load_model
# import numpy as np
#
# np.set_printoptions(suppress=True)
# model = load_model('model.h5')
# data_dir = "./train"
# img_path = "./train/000003/9.jpg"
#
# face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# img = cv2.imread(img_path)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces = face_detector.detectMultiScale(gray, 1.3, 1)
# for (x, y, w, h) in faces:
#     gray = gray[y:y + h, x:x + w]
#     break
#
# resized_img = cv2.resize(gray, (100, 100))
# normalized_img = resized_img / 255.0
# reshaped_img = np.reshape(normalized_img, (1, 100, 100, 1))
# result = model.predict(reshaped_img)
# index = np.argmax(result)
#
# print(result)
# print(index)

from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

model = load_model('model.h5')
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
        './test',
        target_size=(100, 100),
        batch_size=1,
        color_mode="grayscale",
        class_mode='categorical')
score = model.evaluate(test_generator)
print('Test accuracy:', score[1])
