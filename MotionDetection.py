import numpy as np
import cv2

camera = cv2.VideoCapture("parking_test5.mp4")
camera.open("parking_test5.mp4")




while True:
    ret, frame = camera.read()

    # drawing the spots
    Lot1 = cv2.circle(frame, (195, 386), 10, (0, 0, 255), 1, )
    Lot2 = cv2.circle(frame, (239, 385), 10, (0, 0, 225), 1)
    Lot3 = cv2.circle(frame, (263, 365), 10, (0, 0, 225), 1)
    Lot4 = cv2.circle(frame, (239, 385), 10, (0, 0, 225), 1)
    Lot5 = cv2.circle(frame, (298, 353), 10, (0, 0, 225), 1)
    Lot6 = cv2.circle(frame, (325, 339), 10, (0, 0, 225), 1)
    Lot7 = cv2.circle(frame, (356, 328), 10, (0, 0, 225), 1)
    Lot8 = cv2.circle(frame, (385, 314), 10, (0, 0, 225), 1)
    Lot9 = cv2.circle(frame, (403, 303), 10, (0, 0, 225), 1)
    Lot10 = cv2.circle(frame, (438, 294), 10, (0, 0, 225), 1)
    Lot11 = cv2.circle(frame, (468, 279), 10, (0, 0, 225), 1)

    cv2.imshow("Frame", frame)
    


    #define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#release cv2
camera.release()
cv2.destroyAllWindows()


