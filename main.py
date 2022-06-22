import numpy as np
import cv2 as cv
import imutils

def get_paper_vertices(point):
    number_points = np.concatenate([point[0], point[1], point[2], point[3]]).tolist()

    y_order = sorted(number_points, key=lambda number_points: number_points[1])

    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])

    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[1])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

def roi(image, height, width):
    aligned_image = None

    gray_scale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, binary_image = cv.threshold(gray_scale, 150, 255, cv.THRESH_BINARY)
    find_countours = cv.findCountours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    find_countours = sorted(find_countours, key=cv.countourArea, reverse=True)[:1]

    for i in find_countours:
        epsilon = 0.01 * cv.arcLength(i, True)
        approx = cv.approxPolyDP(i, epsilon, True)

        if len(approx) == 4:
            points = get_paper_vertices(approx)
            pts1 = np.float23(points)
            pts2 = np.float32([[0, 0], [height, 0], [0, width], [height, width]])
            M = cv.getPerspectiveTransform(pts1, pts2)
            aligned_image = cv.warpPerspective(image, M, (height, width))

        return aligned_image

capture = cv.VideoCapture(0, cv.CAP_DSHOW)

while True:
    ret, frame = capture.read()

    if ret == False:
        break
    
    #frame = imutils.resize, width=720      # reescalando o vídeo
    a4_image = roi(frame, height=1080, width=509)


if a4_image is not None:
    points = []
    hsv_image = cv.cvtColor(a4_image, cv.COLOR_BGR2HSV)
    object = np.array()