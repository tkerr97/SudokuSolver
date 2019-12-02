import cv2
import tensorflow as tf
import solver
import numpy as np

def performImageActions(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (13,13),0)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 0);
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    image = cv2.erode(image, structuringElement)
    return image


def warpImageToCorners(threshImage, image):

    squareCorners = np.array([[0, 0], [495, 0], [495, 495], [0, 495]], dtype="float32")
    edges = cv2.Canny(threshImage, 10, 100, 5);
    cv2.imshow('edges', edges)
    cv2.waitKey(0)
    contours, h = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE);
    max = 0
    print(len(h))
    bigCountour = []
    for c in contours:
        if cv2.contourArea(c) > max:
            bigContour = c;
            max = cv2.contourArea(bigContour)
    
    border = cv2.boundingRect(bigContour)
    width = border[0] - border[2]
    height = border[1] - border[3]
    print(border)
    print(width)
    print(height)
    tr = np.array([border[0] + width, border[1]], dtype="float32")
    bl = np.array([border[0], border[1] + height], dtype="float32")
    corners = np.array([[border[0], border[1]], tr, [border[2], border[3]], bl], dtype="float32")
    transform = cv2.getPerspectiveTransform(corners,squareCorners)
    image = cv2.warpPerspective(image, transform, (495, 495))
    cv2.imshow('image', image)
    cv2.waitKey(0)
    return image

def findNumbers(image, model):
    numbers = []
    for i in range(1,10):
        row = []
        for j in range(1,10):
            region = cv2.rectangle(i * 55, j * 55, 55, 55)
            number = image[i*55:(i*55)+55,j*55:(j*55)+55]
            number = np.reshape(number, (1,55,55,3))
            cv2.imshow('number',number)
            cv2.waitKey(0)
            number = number.astype('float32')
            row.append(np.argmax(model.predict(number)))
        numbers.append(row)
    return numbers

image = cv2.imread('images/image19.jpg')
model = tf.keras.models.load_model('model.h5')
threshImage = performImageActions(image)
image = warpImageToCorners(threshImage, image)
numbers = findNumbers(image, model)
solver = solver.board(numbers)
solved = solver.solve_recursive()