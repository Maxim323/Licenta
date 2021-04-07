
import cv2
import time
import numpy as np
tpPointsChoose = []
drawing = False
tempFlag = False
Points = []
firstFrame = True
Lot = [''] * 25
ParkingSpaces = []
def draw_ROI(event, x, y, flags, param):
    global point1, tpPointsChoose,pts,drawing, tempFlag, Points


    #desenare puncte cu click stanga
    if event == cv2.EVENT_LBUTTONDOWN:
        tempFlag = True
        drawing = False
        point1 = (x, y)
        tpPointsChoose.append((x, y))  # Used to draw points

    # salvare puncte si inchidere forma cu click dreapta
    if event == cv2.EVENT_RBUTTONDOWN:
        tempFlag = True
        drawing = True
        pts = np.array([tpPointsChoose], np.int32)
        pts1 = tpPointsChoose[1:len(tpPointsChoose)]
        Points.append(tpPointsChoose)
        tpPointsChoose = []
        print(Points)

    # resetare forme cu apasa pe rotita de mouse
    if event == cv2.EVENT_MBUTTONDOWN:
        tempFlag = False
        drawing = True
        tpPointsChoose = []

#detalii ititializare click event + fisier
cv2.namedWindow('Selectare locuri parcare')
cv2.setMouseCallback('Selectare locuri parcare',draw_ROI)
cap = cv2.VideoCapture('testing.mp4')
# Delayed playback, adjusted according to computing power
fps=cap.get(cv2.CAP_PROP_FPS)
size=(cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("fps: {}\nsize: {}".format(fps,size))
vfps = 0.7/fps

while True:
    # capture frame-by-frame
    ret, frame = cap.read()

    while firstFrame is True:
        cv2.imshow('Selectare locuri parcare', frame)

        #Mouse click - stanga
        if (tempFlag == True and drawing == False) :

            #desenare cerc dupa prima apasare a primului punct
            cv2.circle(frame, point1, 5, (0, 255, 0), 2)

            #deneaza linie de la punctul anterior pana la cel apasat curent
            for i in range(len(tpPointsChoose) - 1):
                cv2.line(frame, tpPointsChoose[i], tpPointsChoose[i + 1], (255, 0, 0), 2)

        # Mouse click - dreapta
        if (tempFlag == True and drawing == True):

            #creare polyline cu coordonatele acumulate in [pts] + inchidere forma cu primul punct
            cv2.polylines(frame, [pts], True, (0, 0, 255), thickness=2)

        # Middle mouse button - stergere + creare linie goale, pts devine 0
        if (tempFlag == False and drawing == True):
            for i in range(len(tpPointsChoose) - 1):
                cv2.line(frame, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
                Points = []


        if cv2.waitKey(1) & 0xFF == ord('c'):
            firstFrame = False
            cv2.destroyWindow('Selectare locuri parcare')
            break

    cv2.imshow('CAMERA LIVE PARCARE', frame)
    # creare frame-uri individuale cu coordinatele gasite mai sus
    for m in range(len(ParkingSpaces)):
        for j in range(len(ParkingSpaces[i])):
            Lot[i] = frame[ParkingSpaces[i][1]:ParkingSpaces[i][3], ParkingSpaces[i][0]:ParkingSpaces[i][2]]

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when everything done , release the capture
cap.release()
cv2.destroyAllWindows()