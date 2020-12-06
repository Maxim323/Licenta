import cv2
ParkingSpaces = []
# initial points (before drawing) & other variables
pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
bottomRight_clicked = False
firstFrame = True


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
                print(ParkingSpaces)


#capture video
cap = cv2.VideoCapture('parking_test6.mp4')



while True:
    ret, frame = cap.read()

    while firstFrame is True:



        cv2.namedWindow(winname='myName')
        cv2.setMouseCallback('myName', draw_rectangle)
        cv2.imshow('myName', frame)

        if topLeft_clicked and bottomRight_clicked:
            cv2.rectangle(frame, pt1, pt2, (255,0,0), 2)

        if cv2.waitKey(1) &0xFF == ord('c'):
            firstFrame = False
            break

    #for i in len(ParkingSpaces):

    cv2.imshow('myName', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()