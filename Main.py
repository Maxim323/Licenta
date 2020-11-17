import numpy as np
import cv2

camera = cv2.VideoCapture("parking_test.mp4")
camera.open("parking_test.mp4")


while True:
    ret, frame = camera.read()
    cv2.imshow('CameraFeed',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release cv2
camera.release()
cv2.destroyAllWindows()


