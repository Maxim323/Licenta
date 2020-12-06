# recunoastere linii de parcare dupa culoare
import cv2
import numpy as np


def nothing(x):
    pass


# importare video
camera = cv2.VideoCapture("parking_test2.mp4")
q
# definire trackbars + valorile max & min
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L – H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L – S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L – V", "Trackbars", 169, 255, nothing)
cv2.createTrackbar("U – H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U – S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U – V", "Trackbars", 255, 255, nothing)

while True:
    _, frame = camera.read()

    # filtru de hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # take values from the trackbars
    l_h = cv2.getTrackbarPos("L – H", "Trackbars")
    l_s = cv2.getTrackbarPos("L – S", "Trackbars")
    l_v = cv2.getTrackbarPos("L – V", "Trackbars")
    u_h = cv2.getTrackbarPos("U – H", "Trackbars")
    u_s = cv2.getTrackbarPos("U – S", "Trackbars")
    u_v = cv2.getTrackbarPos("U – V", "Trackbars")

    # stocare valorile date prin trackbar intr-un array
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])

    # aplicare valori array pe o masca
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # operatie de si intre sursa si masca
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # algortim canny cu valori automate
    sigma = 0.3
    median = np.median(frame)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255, (1.0 + sigma) * median))
    autocanny = cv2.Canny(result, lowerThreshold, upperThreshold)

    # afisare feed-uri video
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    cv2.imshow('Autocanny', autocanny)

    # define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release cv2
camera.release()
cv2.destroyAllWindows()
