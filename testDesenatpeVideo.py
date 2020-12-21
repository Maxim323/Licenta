import cv2

import numpy as np

ParkingSpaces = []
# initial points (before drawing) & other variables
pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
bottomRight_clicked = False
firstFrame = True
Lot = ['']*10
contours = ['']*10
hierarchy = ['']*10
area= ['']*10
sts=['']*10
cnt=['']*10


#mouse callback function#
def draw_rectangle(event, x, y, flags, param):

    global pt1, pt2, topLeft_clicked, bottomRight_clicked

    #mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        #reset
        if topLeft_clicked and bottomRight_clicked:
            topLeft_clicked = False
            bottomRight_clicked = False
            pt1 = (0,0)
            pt2 = (0,0)
        #get coordinates of top left corner
        if not topLeft_clicked:
            pt1 = (x,y)
            topLeft_clicked = True
        #get coordinates of bottom right corner
        elif not bottomRight_clicked:
            pt2 = (x,y)
            bottomRight_clicked = True

            if firstFrame is True:
                ParkingSpaces.append(pt1 + pt2)

                #printare dreptunghiurile desenate pe video
                print(ParkingSpaces)



#capture video
cap = cv2.VideoCapture('parking_test.mp4')

while True:
    ret, frame = cap.read()

    # procesare imagine
    grayFilter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # autocanny
    sigma = 0.3
    median = np.median(frame)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255, (1.0 + sigma) * median))

    edge = cv2.Canny(grayFilter, lowerThreshold, upperThreshold)

    _, FinalFrame = cv2.threshold(edge, 80, 255, cv2.THRESH_BINARY)

    while firstFrame is True:

        cv2.namedWindow(winname='myName')
        cv2.setMouseCallback('myName', draw_rectangle)
        cv2.imshow('myName', frame)

        if topLeft_clicked and bottomRight_clicked:
            cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            firstFrame = False
            break

    for i in range(len(ParkingSpaces)):
        for j in range(len(ParkingSpaces[i])):
            Lot[i] = FinalFrame[ParkingSpaces[i][1]:ParkingSpaces[i][3], ParkingSpaces[i][0]:ParkingSpaces[i][2]]


    for m in range(len(ParkingSpaces)):
            contours[m], _ = cv2.findContours(Lot[m], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i in range(len(ParkingSpaces)):
        for cnt[i] in contours[i]:
            area[i] = cv2.contourArea(cnt[i])
            if area[i] > 1:
                sts[i] = "OCUPAT"
            else:
                sts[i] = "LIBER"
    print(sts)
    print(area)


    cv2.imshow('myName', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
