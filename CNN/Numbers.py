import numpy as np
import sklearn.model_selection as sk
from PIL import Image
from os import path

import tensorflow as tf

# Read in and reshape the images
images = []
labels = []
f = open('data/data.txt', 'r')
#for i in range(1, 1089):
#    for j in range(1, 9):
#        for k in range(1, 9):
#            file = 'data/' + str(i) + '-' + str(j) + ',' + str(k) + '.jpg'
#            if path.exists(file):
#                image = Image.open(file)
#                images.append(np.array(image))
#                image.load()
#                c = f.read(1)
#                labels.append(int(c))
#                c = f.read(1)
#            else:
#                continue
#labels = np.array(labels)
#images = np.array(images).astype("float32")
#numbers /= 255

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data();
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

# Split the labels and images into train and test
#train_images, test_images, train_labels, test_labels = sk.train_test_split(images, labels, test_size=.2)
#(images.shape)
# Set up the layers of the model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28,28,1)),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(2048, activation='relu'),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(2048, activation='relu'),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Check that TF is running on the GPU
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

# Train the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=3)

# Check the statistics
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Accuracy: ", test_acc)

model.save("model.h5", include_optimizer=False)
