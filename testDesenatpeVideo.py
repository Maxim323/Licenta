from typing import List, Tuple

import cv2
import numpy as np
from datetime import datetime
import time
from threading import Thread
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo



# initial points (before drawing) & other variables

pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
bottomRight_clicked = False
firstFrame = True
Start = True

# stocare fiecare frame selectat
Lot = [''] * 25
NumberingLots = [''] * 25
MaskedFrame = ['']*25
contours = [''] * 25
hierarchy = [''] * 25

# nr conture pt fiecare zona selectata
area = [''] * 25

# OCUPAT / LIBER pt fiecare loc de parcare selectat
sts = [''] * 25

# conture pentru fiecare loc de parcare selectat
cnt = [''] * 25

# lista pt stocare valori de pixeli albi pt fiecare loc de paracare individual
WhitePixels = [''] * 25

# ora parcare masina
ParkedHour = [''] * 25

tpPointsChoose = []
drawing = False
tempFlag = False


firstFrame = True
Lot = [''] * 25
ParkingSpaces = []
Points = []
FirstFramePoint = [''] * 25
SecondFramePoint = [''] * 25
ParkingSpaces = [''] * 25
varTest = [''] * 25

def GetData():
    while True:

        BusyParkingSpaces = 0
        TrueRange = 0

        for h in range(len(sts)):
            if sts[h] == "OCUPAT":
                BusyParkingSpaces = BusyParkingSpaces + 1

        for g in range(len(sts)):
            if sts[h] == "LIBER" or sts[h] == "OCUPAT":
                TrueRange = TrueRange + 1

        TotalParkingSpaces = int(len(sts))
        FreeParkingSpaces = TotalParkingSpaces - BusyParkingSpaces

        # reading excel data file
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Data"
        # creating hearders
        headers = ["Lot", "Status", "Date&Time", "BusySpaces", "FreeSpaces"]

        for m in range(len(ParkingSpaces)):
            # headers
            sheet["A1"] = headers[0]
            sheet["B1"] = headers[1]
            sheet["C1"] = headers[2]
            sheet["D1"] = headers[3]
            sheet["E1"] = headers[4]

            # data
            sheet["A" + str(m + 2)] = NumberingLots[m]
            sheet["B" + str(m + 2)] = sts[m]
            sheet["C" + str(m + 2)] = ParkedHour[m]
            sheet["D" + str(m + 2)] = BusyParkingSpaces
            sheet["E" + str(m + 2)] = FreeParkingSpaces

        # creating a table
        tab = Table(displayName="Table1", ref="A1:E" + str(len(ParkingSpaces) + 1))

        # defining tabler style
        style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                               showLastColumn=False, showRowStripes=True, showColumnStripes=True)

        # apply style
        tab.tableStyleInfo = style

        # adaugare table la sheet
        sheet.add_table(tab)

        # salvare fisier
        workbook.save(filename="Data.xlsx")

        # printare tranfer cu succes
        print("Data transfer done")

        #scriere in fisier odata la 10sec
        time.sleep(10)

        if cv2.waitKey(1) & 0xFF == ord('q'):
         break

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


# getting the current time outside main loop
now = datetime.now()

# current time are full data format pt procesare date
current_time = now.strftime("%m-%d-%Y %H:%M:%S")


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



        if cv2.waitKey(1) & 0xFF == ord('c'):
            firstFrame = False
            cv2.destroyWindow('Selectare locuri parcare')
            break

    #filtru aplicat cu succes - iterativ
    for i in range(len(Points)):

        mask = np.zeros(frame.shape, dtype=np.uint8)
        roi_corners = np.array([Points[i]], dtype=np.int32)
        white = (255, 255, 255)
        cv2.fillPoly(mask, roi_corners, white)

        #stocare locatii masini din 4 puncte + masca negru adaugata peste excese intr-un singur frame pt procesare
        MaskedFrame[i] = cv2.bitwise_and(frame, mask)



    #acum greul.......fuck my life
    #asignare puncte inceput
    #ceva ciudat se intampla aici..
    for a in range(len(Points)):
        FirstFramePoint[a] = Points[a][1]
        SecondFramePoint[a] = Points[a][2]
        ParkingSpaces[a] = FirstFramePoint[a] + SecondFramePoint[a]


    #TypeError: list indices must be integers or slices, not tuple
    for v in range(len(varTest)):
        Lot[v] = MaskedFrame[varTest[v][1]:varTest[v][3], varTest[v][0]:varTest[v][2]]

    #cv2.imshow('test', Lot[0])

    # #verificare axa x si y colt stanga sus - primul punct pt frame nou
    # for i in range(len(Points)):
    #     if FirstFramePoint[i] < Points[i][1]:
    #         FirstFramePoint[i] = Points[i][1]
    #
    #     if FirstFramePoint[i] > Points[i][1]:
    #         FirstFramePoint[i] = Points[i][1]
    #
    # # verificare axa x si y colt drepta jos - al 2lea punct pt frame nou
    # for i in range(len(Points)):
    #     if SecondFramePoint[i] < Points[i][3]:
    #         SecondFramePoint[i] = Points[i][3]
    #
    #     if SecondFramePoint[i] > Points[i][3]:
    #         SecondFramePoint[i] = Points[i][3]




    #(123, 145), (86, 346), (509, 394), (585, 125)
    #FirstFramePoint = (123, 145)(509, 394)
    #SecondFramePoint(509, 394)

    # de la x asta pana la x alalalt, de la y asta pana la y alalalt
    #ParkingSpaces[i][1]: ParkingSpaces[i][3], ParkingSpaces[i][0]: ParkingSpaces[i][2]




    #printare detalii - pt dev
    # print('Locuri libere de parcare:',FreeParkingSpaces)
    # print(sts)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when everything done , release the capture
cap.release()
cv2.destroyAllWindows()