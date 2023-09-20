from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.optimizers import Adam
from keras.regularizers import l2
from matplotlib import pyplot as plt


def train():
    # 数据增强
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        fill_mode='nearest',
        validation_split=0.2)

    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        './train',
        target_size=(100, 100),
        batch_size=16,
        subset='training',
        color_mode="grayscale",
        class_mode='categorical')

    validation_generator = train_datagen.flow_from_directory(
        './train',
        target_size=(100, 100),
        batch_size=16,
        subset='validation',
        color_mode="grayscale",
        class_mode='categorical')

    test_generator = test_datagen.flow_from_directory(
        './test',
        target_size=(100, 100),
        batch_size=16,
        color_mode="grayscale",
        class_mode='categorical')

    # 构建CNN模型
    model = Sequential()
    # 第一层卷积
    model.add(Conv2D(32, (3, 3), input_shape=(100, 100, 1), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 第二层卷积
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    # 第三层卷积
    model.add(Conv2D(128, (3, 3), activation="relu", kernel_regularizer=l2(0.01)))
    model.add(Dropout(0.3))
    model.add(Flatten())
    # 全连接1
    model.add(Dense(256, activation="relu", kernel_regularizer=l2(0.01)))
    model.add(Dropout(0.4))
    # 全连接2
    model.add(Dense(train_generator.num_classes, activation="softmax"))
    # 编译模型
    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.0001), metrics=['accuracy'])
    model.summary()

    epoch = 30
    # 训练模型
    history = model.fit(
            train_generator,
            steps_per_epoch=train_generator.n//epoch,
            shuffle=True,
            epochs=epoch,
            verbose=2,
            validation_data=validation_generator
            )

    score = model.evaluate(test_generator)
    print('Test accuracy:', score[1])
    model.save('model.h5')

    # 绘制训练集和验证集的损失曲线
    plt.figure()
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.title('Model loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # 绘制训练集和验证集的准确率曲线
    plt.figure()
    plt.plot(history.history['accuracy'], label='train_acc')
    plt.plot(history.history['val_accuracy'], label='val_acc')
    plt.title('Model accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()


train()
