import numpy as np
import cv2

camera = cv2.VideoCapture('testing.mp4')

while True:
    ret, frame = camera.read()

    # autocanny
    sigma = 0.3
    median = np.median(frame)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255, (1.0 + sigma) * median))

    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(frame, kernel, iterations=1)
    autocanny_dilat = cv2.Canny(dilation, lowerThreshold, upperThreshold)

    cv2.imshow("autocanny_dilat",autocanny_dilat)




    #define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#release cv2
camera.release()
cv2.destroyAllWindows()


