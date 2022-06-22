import numpy as np
# import cv2
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

    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_scale, 150, 255, cv2.THRESH_BINARY)
    find_countours = cv2.findCountours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    find_countours = sorted(find_countours, key=cv2.countourArea, reverse=True)[:1]

    for i in find_countours:
        epsilon = 0.01 * cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, epsilon, True)

        if len(approx) == 4:
            points = get_paper_vertices(approx)
            pts1 = np.float23(points)
            pts2 = np.float32([[0, 0], [height, 0], [0, width], [height, width]])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            aligned_image = cv2.warpPerspective(image, M, (height, width))

        return aligned_image


capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = capture.read()

    if ret == False:
        break
    
    #frame = imutils.resize, width=720      # reescalando o vídeo
    a4_image = roi(frame, height=1080, width=509)