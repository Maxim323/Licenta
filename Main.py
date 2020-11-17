import numpy as np
import cv2

camera = cv2.VideoCapture("parking_test4.mp4")
camera.open("parking_test4.mp4")




while True:
    ret, frame = camera.read()

    #autocanny
    sigma = 0.3
    median = np.median(frame)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255,(1.0 + sigma)*median))

    # converting to grayScale
    grayFilter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    autocanny = cv2.Canny(grayFilter, lowerThreshold,upperThreshold)
    cv2.imshow('Autocanny', autocanny)

    #showing original video
    cv2.imshow('CameraFeed',frame)

    #showing grayScale video
    #cv2.imshow('GrayFilter', grayFilter)

    #cannyEdge detector
    cannyFilter = cv2.Canny(grayFilter, 100, 200)

    #showing cannyEdge video
    #cv2.imshow('CannyFilter', cannyFilter)

    #define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#release cv2
camera.release()
cv2.destroyAllWindows()


