import glob

import numpy as np
import sklearn.model_selection as sk
from os import path
from PIL import Image
import tensorflow as tf
import cv2
import convert_model
from sklearn.utils import shuffle

def getClass(string):
    string = string[5:11]
    classes = {
        'img010': 9,
        'img008': 7,
        'img007': 6,
        'img006': 5,
        'img005': 4,
        'img004': 3,
        'img003': 2,
        'img002': 1,
        'img001': 0,
        'img009': 8,
    }
    return classes[string]

# Read in and reshape the images
images = []
labels = []
f = open('data/data.txt', 'r')
for i in range(0, 1089):
    for j in range(0, 10):
        for k in range(0, 10):
            file = 'data/' + str(i) + '-' + str(j) + ',' + str(k) + '.jpg'
            if path.exists(file):
                img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
               # ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
                images.append(img)

                c = f.read(1)
                labels.append(int(c))
                c = f.read(1)

            else:
                continue
for filename in glob.glob('data/*.png'):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (49, 49), cv2.INTER_CUBIC)
    img = np.pad(img, pad_width=3, mode='constant', constant_values=0)
    img = cv2.bitwise_not(img)
    images.append(img)
    labels.append(getClass(filename))

images = np.array(images)
labels = np.array(labels)
images = np.array(images).astype(np.float32)
images = images.reshape((images.shape[0], 55, 55, 1))
images /= 255

print(images.shape)

# Split the labels and images into train and test
#images, labels = shuffle(images, labels)
train_images, test_images, train_labels, test_labels = sk.train_test_split(images, labels, test_size=.2)
# Set up the layers of the model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(55, 55, 1)),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(2048, activation='relu'),
    tf.keras.layers.Dropout(.5),
    tf.keras.layers.Dense(2048, activation='relu'),
    tf.keras.layers.Dropout(.5),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.summary()
# Check that TF is running on the GPU
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

# Train the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images, train_labels, batch_size=128, epochs=10)

# Check the statistics
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Accuracy: ", test_acc)


print(model.predict(images[0:9]))
model.save("model.h5", include_optimizer=False)
print("Saved model to disk")
convert_model.convert("model.h5", "out.json")
