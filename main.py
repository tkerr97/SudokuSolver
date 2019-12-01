import cv2
import tensorflow as tf
import solver

def performImageActions(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (13,13),0)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 0);
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    image = cv2.erode(image, structuringElement)
    return image


def warpImageToCorners(threshImage, image):

    squareCorners = {(0, 0), (500, 0), (500, 500), (0, 500)}
    edges = cv2.Canny(threshImage, 10, 100, 5);

    countors = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE);
    max = 0

    bigCountour = []
    for contour in countors:
        if cv2.contourArea(contour) > max:
            bigContour = contour;
            max = cv2.contourArea(bigContour)


    border = cv2.boundingRect(bigContour)
    tr = (border.tl().x + border.width, border.tl().y)
    bl = (border.tl().x, border.tl().y + border.height)
    corners = [border.tl(), tr, border.br(), bl]
    transform = cv2.getPerspectiveTransform(corners, squareCorners)
    image = cv2.warpPerspective(image, transform, (500, 500))
    return image

def findNumbers(image, model):
    numbers = []
    for i in range(1,10):
        row = []
        for j in range(1,10):
            region = cv2.Rect(i * 55, j * 55, 55, 55)
            number = cv2.Mat(image, region)
            row.append(model.predict(number))
        numbers.append(row)
    return numbers

image = cv2.imread('../images/image19.jpg')
model = tf.saved_model.load('model/')
threshImage = performImageActions(image)
image = warpImageToCorners(image)
numbers = findNumbers(image, model)
solver = solver.board(numbers)
solved = solver.solve_recursive()