import numpy as np
import cv2

camera = cv2.VideoCapture("parking_test6.mp4")

while True:
    ret, frame = camera.read()

    # procesare imagine
    grayFilter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # autocanny
    sigma = 0.3
    median = np.median(frame)
    lowerThreshold = int(max(0, (1.0 - sigma) * median))
    upperThreshold = int(min(255, (1.0 + sigma) * median))

    edge = cv2.Canny(grayFilter, lowerThreshold, upperThreshold)
    _, threshold2 = cv2.threshold(edge, 80, 255, cv2.THRESH_BINARY)

    # creare frame pentru fiecare loc de parcare
    # [y:y - y stanga sus, y dreapta jos, x:x - asemenea y]
    Lot1 = threshold2[476:531, 38:126]
    Lot2 = threshold2[487:519, 153:212]
    Lot3 = threshold2[483:510, 253:323]
    Lot4 = threshold2[476:508, 354:428]
    Lot5 = threshold2[465:500, 462:483]
    Lot6 = threshold2[467:494, 541:609]
    Lot7 = threshold2[456:486, 633:690]
    Lot8 = threshold2[449:479, 727:767]

    contours1, hierarchy1 = cv2.findContours(Lot1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours2, hierarchy2 = cv2.findContours(Lot2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours3, hierarchy3 = cv2.findContours(Lot3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours4, hierarchy4 = cv2.findContours(Lot4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours5, hierarchy5 = cv2.findContours(Lot5, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours6, hierarchy6 = cv2.findContours(Lot6, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours7, hierarchy7 = cv2.findContours(Lot7, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours8, hierarchy8 = cv2.findContours(Lot8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    stsP1 = stsP2 = stsP3 = stsP4 = stsP5 = stsP6 = stsP7 = stsP8 = ''

    for cnt1 in contours1:
        area1 = cv2.contourArea(cnt1)
        if area1 > 1:
            stsP1 = "OCUPAT"
            cv2.putText(frame, 'P1', (38, 476), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P1', (38, 476), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    for cnt2 in contours2:
        area2 = cv2.contourArea(cnt2)
        if area2 > 1:
            stsP2 = "OCUPAT"
            cv2.putText(frame, 'P2', (153, 487), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P2', (153, 487), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    for cnt3 in contours3:
        area3 = cv2.contourArea(cnt3)
        if area3 > 1:
            stsP3 = "OCUPAT"
            cv2.putText(frame, 'P3', (253, 483), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P3', (253, 483), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    for cnt4 in contours4:
        area4 = cv2.contourArea(cnt4)
        if area4 > 1:
            stsP4 = "OCUPAT"
            cv2.putText(frame, 'P4', (354, 476), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P4', (354, 476), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    for cnt5 in contours5:
        area5 = cv2.contourArea(cnt5)
        if area5 > 1:
            stsP5 = "OCUPAT"
            cv2.putText(frame, 'P5', (462, 465), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P5', (462, 465), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    for cnt6 in contours6:
        area6 = cv2.contourArea(cnt6)
        if area6 > 1:
            stsP6 = "OCUPAT"
            cv2.putText(frame, 'P6', (541, 467), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P6', (541, 467), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    for cnt7 in contours7:
        area7 = cv2.contourArea(cnt7)
        if area7 > 1:
            stsP7 = "OCUPAT"
            cv2.putText(frame, 'P7', (633, 456), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P7', (633, 456), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    for cnt8 in contours8:
        area8 = cv2.contourArea(cnt8)
        if area8 > 1:
            stsP8 = "OCUPAT"
            cv2.putText(frame, 'P8', (727, 449), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_4)
        else:
            cv2.putText(frame, 'P8', (727, 449), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 139, 34), 2, cv2.LINE_4)

    cv2.imshow("OriginalVideo", frame)
    #cv2.imshow("Contur", threshold2)

    print("P1:", stsP1 + " P2:", stsP2 + " P3:", stsP3 + " P4:", stsP4 + " P5:", stsP5 + " P6:", stsP6 + " P7:",
          stsP7 + " P8:", stsP8)

    # define exit program key (q)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release cv2
camera.release()
cv2.destroyAllWindows()
