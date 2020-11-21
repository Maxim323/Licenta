import numpy as np
import cv2

camera = cv2.VideoCapture("parking_test5.mp4")
camera.open("parking_test5.mp4")


while True:
    ret, frame = camera.read()

    grayFilter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

 #incercare detectare diferenta de nr conture
    frame2 = grayFilter[272:321,366:466]
    _, threshold2 = cv2.threshold(frame2, 80, 255, cv2.THRESH_BINARY)

    cv2.imshow("Frame2", threshold2)

    contours, hierarchy= cv2.findContours(threshold2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)

        area = cv2.contourArea(cnt)
        if area < 4752:
            print("Loc ocupat!")
            cv2.rectangle(threshold2,(x,y),(x+w, y+h),(0,0,255),2)
        elif area >= 4752:
            print("Loc liber")
            cv2.rectangle(threshold2, (x, y), (x + w, y + h), (0, 0, 255), 2)



    #define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#release cv2
camera.release()
cv2.destroyAllWindows()


