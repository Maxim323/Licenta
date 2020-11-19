import numpy as np
import cv2

camera = cv2.VideoCapture("parking_test5.mp4")
camera.open("parking_test5.mp4")




while True:
    ret, frame = camera.read()

    # define area to be used
    # x = 12 y = 7
    # x = 1261 y 816
    CarSpots = frame[7: 816, 12: 1261]

    #autocanny
    sigma = 0.3
    median = np.median(CarSpots)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255,(1.0 + sigma)*median))

    # converting to grayScale
    grayFilter = cv2.cvtColor(CarSpots, cv2.COLOR_BGR2GRAY)
    autocanny = cv2.Canny(grayFilter, lowerThreshold, upperThreshold)

    # binary image
    _, threshold = cv2.threshold(autocanny, 80, 255, cv2.THRESH_BINARY)

    firstlot = image = cv2.rectangle(frame, (255, 396), (309, 423), (0, 89, 192), 5)


    #showing original video
    cv2.imshow('CameraFeed',frame)
   #  cv2.imshow("BinaryFilter", threshold+ firstlot)
    cv2.imshow("Lots",  firstlot)

    #showing grayScale video
    #cv2.imshow('GrayFilter', grayFilter)

    #cannyEdge detector
    #cannyFilter = cv2.Canny(grayFilter, 100, 200)

    #showing cannyEdge video
    #cv2.imshow('CannyFilter', cannyFilter)

    #define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#release cv2
camera.release()
cv2.destroyAllWindows()


