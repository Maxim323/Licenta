# selecteaza stream video
# selecteaza locurile de parcare din primul frame
# dupa selectare locuri parcare pe care le doresti sa fie monitorizate apasa "c"
# apasa "q" cand vrei sa inchizi programul

import cv2
import numpy as np
from datetime import datetime

ParkingSpaces = []
# initial points (before drawing) & other variables
pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
bottomRight_clicked = False
firstFrame = True
Start = True
BusyParkingSpaces = 0
FreeParkingSpaces = 0


#stocare fiecare frame selectat
Lot = ['']*25

contours = ['']*25
hierarchy = ['']*25

#nr conture pt fiecare zona selectata
area= ['']*25

#OCUPAT / LIBER pt fiecare loc de parcare selectat
sts=['']*25

#conture pentru fiecare loc de parcare selectat
cnt=['']*25

#lista pt stocare valori de pixeli albi pt fiecare loc de paracare individual
WhitePixels = ['']*25

#ora parcare masina
ParkedHour = ['']*25

# mouse callback function - do not mess WITH.
def draw_rectangle(event, x, y, flags, param):
    global pt1, pt2, topLeft_clicked, bottomRight_clicked

    # mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        #reset
        if topLeft_clicked and bottomRight_clicked:
            topLeft_clicked = False
            bottomRight_clicked = False
            pt1 = (0, 0)
            pt2 = (0, 0)

        # get coordinates of top left corner
        if not topLeft_clicked:
            pt1 = (x, y)
            topLeft_clicked = True

        # get coordinates of bottom right corner
        elif not bottomRight_clicked:
            pt2 = (x, y)
            bottomRight_clicked = True

            if firstFrame is True:
                ParkingSpaces.append(pt1 + pt2)

                #printare coordonate dreptunghiurile desenate pe video
                print(ParkingSpaces)

# capture video
cap = cv2.VideoCapture('testing.mp4')

#getting the current time outside main loop
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

#main function
while True:

    #stabilire nr max locuri parcare la inceputul programului
    if Start == True:
        demoVar = input("Te rog introdu numarul maxim de locuri de parcare: ")
        TotalParkingSpaces = (int)(demoVar)
        Start = False

    #citire video input
    ret, frame = cap.read()

    #autocanny
    sigma = 0.3
    median = np.median(frame)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255, (1.0 + sigma) * median))

    #creare kernel pt convolutie
    kernel = np.ones((5, 5), np.uint8)

    #operatie de dilatare video cu kernelul creat
    dilation = cv2.dilate(frame, kernel, iterations=1)

    #canny cu frame-ul rezultat din dilatare
    edge = cv2.Canny(dilation, lowerThreshold, upperThreshold)

    #conversie catre frame binar dupa canny pt accuracy mai mare
    _, FinalFrame = cv2.threshold(edge, 80, 255, cv2.THRESH_BINARY)

    #gasire coordonate locuri de parcare selectate
    while firstFrame is True:

        cv2.namedWindow(winname='myName')
        cv2.setMouseCallback('myName', draw_rectangle)
        cv2.imshow('myName', frame)

        if topLeft_clicked and bottomRight_clicked:
            cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            firstFrame = False
            break

    #creare frame-uri individuale cu coordinatele gasite mai sus
    for i in range(len(ParkingSpaces)):
        for j in range(len(ParkingSpaces[i])):
            Lot[i] = FinalFrame[ParkingSpaces[i][1]:ParkingSpaces[i][3], ParkingSpaces[i][0]:ParkingSpaces[i][2]]

    #cautare pixeli albi in loturile de parcare generate
    for m in range(len(ParkingSpaces)):
      WhitePixels[m] =cv2.countNonZero(Lot[m])


    #stabilire loc ocupat / liber in functie de nr de pixeli albi gasiti
    for i in range(len(ParkingSpaces)):
            if WhitePixels[i] >= 1000:
                sts[i] = "OCUPAT"
                ParkedHour[i] = current_time
            else:
                sts[i] = "LIBER"
                ParkedHour[i] = 0

    BusyParkingSpaces = 0
    for h in range(len(sts)):
        if sts[h] == "OCUPAT":
            BusyParkingSpaces = BusyParkingSpaces + 1

    FreeParkingSpaces = TotalParkingSpaces - BusyParkingSpaces

    #printare detalii - pt dev
    #cv2.imshow('Procesare', FinalFrame)
    #print('Locuri libere de parcare:',FreeParkingSpaces)
    print(ParkedHour)
    print(sts)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()
