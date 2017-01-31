import cv2

import numpy as np



cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use

cv2.namedWindow('result')
cv2.namedWindow('frame')

# Starting with 100's to prevent error while masking

#h,s,v = 100,100,100
# Creating track bar

cv2.createTrackbar('h_min', 'result',0,180,nothing)
cv2.createTrackbar('s_min', 'result',0,255,nothing)
cv2.createTrackbar('v_min', 'result',0,255,nothing)
cv2.createTrackbar('h_max', 'result',0,180,nothing)
cv2.createTrackbar('s_max', 'result',0,255,nothing)
cv2.createTrackbar('v_max', 'result',0,255,nothing)
cv2.createTrackbar('blur', 'result',1,20,nothing)
while(1):
    ret, frame = cap.read()
    if not ret: continue
    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h_min','result')
    s = cv2.getTrackbarPos('s_min','result')
    v = cv2.getTrackbarPos('v_min','result')
    h2 = cv2.getTrackbarPos('h_max','result')
    s2 = cv2.getTrackbarPos('s_max','result')
    v2 = cv2.getTrackbarPos('v_max','result')
    b = cv2.getTrackbarPos('blur','result')

    # prevent blur value from equalling 0.... bad juju
    if b == 0:
        b = 1
    #frame = cv2.GaussianBlur(frame, (2*b-1,2*b-1), 0)
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # Normal masking algorithm
    lower = np.array([h,s,v])
    upper = np.array([h2,s2,v2])
    # Create the color mask
    mask = cv2.inRange(hsv,lower, upper)
    # Find the contours
    image,contours,hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # finding contour with maximum area and store it as best_cnt
    best_cnt = 0
    max_area = 0
    areaArray = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        areaArray.append(area)
    # Generate the result frame
    result = cv2.bitwise_and(frame,frame,mask = mask)
    # Find and draw the largest contour
    sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
    if len(sorteddata) != 0:
        best_cnt = sorteddata[0][1]
        x, y, w, h = cv2.boundingRect(best_cnt)
        cv2.drawContours(result, best_cnt, -1, (255, 0, 0), 2)
        cv2.rectangle(result, (x, y), (x+w, y+h), (0,255,0), 2)
    cv2.imshow('frame',frame)
    cv2.imshow('result',result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
