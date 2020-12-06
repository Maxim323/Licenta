import numpy as np
import cv2

point1 = ()
point2 = ()
drawing = False


def mouse_drawing(event, x, y, flags, param):
    global point1, point2, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing is False:
            drawing = True
            point1 = (x, y)
        else:
            drawing = False

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            point2 = (x, y)


camera = cv2.VideoCapture("parking_test6.mp4")
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

while True:
    ret, frame = camera.read()

    if point1 and point2:
        cv2.rectangle(frame, point1, point2, (0.255, 0), 2)



    cv2.imshow("Frame", frame)


    # define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release cv2
camera.release()
cv2.destroyAllWindows()
