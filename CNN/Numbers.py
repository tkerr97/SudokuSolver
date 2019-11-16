import numpy as np
import sklearn.model_selection as sk
import matplotlib.image as mpimg
from os import path

import tensorflow as tf

# Read in and reshape the images
images = []
labels = np.empty((12992,))
f = open('data/data.txt', 'r')
for i in range(1, 1089):
    for j in range(1, 9):
        for k in range(1, 9):
            if path.exists('data/' + str(i) + '-' + str(j) + ',' + str(k) + '.jpg'):
                images.append(mpimg.imread('data/' + str(i) + '-' + str(j) + ',' + str(k) + '.jpg'))
                c = f.read(1)
                np.append(labels, int(c))
                c = f.read(1)
            else:
                continue
images = np.array(images).astype(np.float32)

# Split the labels and images into train and test
train_images, test_images, train_labels, test_labels = sk.train_test_split(images, labels, test_size=.25)
print(images.shape)
# Set up the layers of the model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
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
model.fit(train_images, train_labels, epochs=3)

# Check the statistics
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Accuracy: ", test_acc)

# Save model to file
model_json = model.to_json()
with open("numbers.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("numbers.h5")
print("Saved model to disk")
