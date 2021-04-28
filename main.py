# selecteaza stream video
# selecteaza locurile de parcare din primul frame
# dupa selectare locuri parcare pe care le doresti sa fie monitorizate apasa "c"
# apasa "q" cand vrei sa inchizi programul

import time
from datetime import datetime

import cv2
import numpy as np
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

# stocare fiecare frame selectat
Lot = [''] * 25
NumberingLots = [''] * 25
MaskedFrame = [''] * 25

# OCUPAT / LIBER pt fiecare loc de parcare selectat
sts = [''] * 25

# lista pt stocare valori de pixeli albi pt fiecare loc de paracare individual
WhitePixels = [''] * 25

# ora parcare masina
ParkedHour = [''] * 25

tpPointsChoose = []
drawing = False
tempFlag = False
firstFrame = True
Points = []
ParkingSpaces = [''] * 25


def getData():
    while True:

        BusyParkingSpaces = 0

        for h in range(len(sts)):
            if sts[h] == "OCUPAT":
                BusyParkingSpaces = BusyParkingSpaces + 1

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

        # scriere in fisier odata la 10sec
        time.sleep(10)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def draw_ROI(event, x, y, flags, param):
    global point1, tpPointsChoose, pts, drawing, tempFlag, Points

    # desenare puncte cu click stanga
    if event == cv2.EVENT_LBUTTONDOWN:
        tempFlag = True
        drawing = False
        point1 = (x, y)
        tpPointsChoose.append((x, y))

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

# detalii ititializare click event + fisier
cv2.namedWindow('Selectare locuri parcare')
cv2.setMouseCallback('Selectare locuri parcare', draw_ROI)

cap = cv2.VideoCapture('testing.mp4')

# Delayed playback, adjusted according to computing power
fps = cap.get(cv2.CAP_PROP_FPS)
size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("fps: {}\nsize: {}".format(fps, size))
vfps = 0.7 / fps

while True:
    # capture frame-by-frame
    ret, frame = cap.read()

    # autocanny
    sigma = 0.3
    median = np.median(frame)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255, (1.0 + sigma) * median))

    # creare kernel pt convolutie
    kernel = np.ones((5, 5), np.uint8)

    # operatie de dilatare video cu kernelul creat
    dilation = cv2.dilate(frame, kernel, iterations=1)

    # canny cu frame-ul rezultat din dilatare
    edge = cv2.Canny(dilation, lowerThreshold, upperThreshold)

    # conversie catre frame binar dupa canny pt accuracy mai mare
    _, FinalFrame = cv2.threshold(edge, 80, 255, cv2.THRESH_BINARY)

    while firstFrame is True:
        cv2.imshow('Selectare locuri parcare', frame)

        # Mouse click - stanga
        if (tempFlag == True and drawing == False):

            # desenare cerc dupa prima apasare a primului punct
            cv2.circle(frame, point1, 5, (0, 255, 0), 2)

            # deneaza linie de la punctul anterior pana la cel apasat curent
            for i in range(len(tpPointsChoose) - 1):
                cv2.line(frame, tpPointsChoose[i], tpPointsChoose[i + 1], (255, 0, 0), 2)

        # Mouse click - dreapta
        if (tempFlag == True and drawing == True):
            # creare polyline cu coordonatele acumulate in [pts] + inchidere forma cu primul punct
            cv2.polylines(frame, [pts], True, (0, 0, 255), thickness=2)

        # Middle mouse button - stergere + creare linie goale, pts devine 0
        if (tempFlag == False and drawing == True):
            for i in range(len(tpPointsChoose) - 1):
                cv2.line(frame, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            firstFrame = False
            cv2.destroyWindow('Selectare locuri parcare')
            break

    # filtru aplicat cu succes - iterativ
    for i in range(len(Points)):
        mask = np.zeros(FinalFrame.shape, dtype=np.uint8)
        roi_corners = np.array([Points[i]], dtype=np.int32)
        white = (255, 255, 255)
        cv2.fillPoly(mask, roi_corners, white)

        # stocare locatii masini din 4 puncte + masca negru adaugata peste excese intr-un singur frame pt procesare
        MaskedFrame[i] = cv2.bitwise_and(FinalFrame, mask)

        WhitePixels[i] = cv2.countNonZero(MaskedFrame[i])

        # stabilire loc ocupat / liber in functie de nr de pixeli albi gasiti
    for i in range(len(ParkingSpaces)):
        if WhitePixels[i] != '':
            if WhitePixels[i] >= 1000:
                sts[i] = "OCUPAT"
                ParkedHour[i] = current_time
            else:
                sts[i] = "LIBER"
                ParkedHour[i] = 0

    cv2.imshow('test1', FinalFrame)
    print(sts)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
