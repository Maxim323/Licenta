import numpy as np
import cv2

camera = cv2.VideoCapture("parking_test.mp4")
camera.open("parking_test.mp4")

while True:
    ret, frame = camera.read()

    #showing original video
    cv2.imshow('CameraFeed',frame)

    #converting to grayScale
    grayFilter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #showing grayScale video
    cv2.imshow('GrayFilter', grayFilter)

    #define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#release cv2
camera.release()
cv2.destroyAllWindows()


