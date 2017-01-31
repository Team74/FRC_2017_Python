import cv2
import numpy as np

cv2.namedWindow("frame")
cv2.namedWindow("new")
cv2.namedWindow("green")

cap = cv2.VideoCapture(0)

lower_g = np.array([65, 180, 180])
upper_g = np.array([85, 255, 255])

while(True):
	ret, frame = cap.read()
	#frame = cv2.blur(frame, (10,10))

	g_in = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	g_mask = cv2.inRange(g_in, lower_g, upper_g)
	g_res = cv2.bitwise_and(frame, frame, mask= g_mask)

	kernel = np.ones((5,5), np.uint8)
	g_thresh = cv2.dilate(g_mask, kernel, iterations = 3)
	g_thresh = cv2.erode(g_thresh, kernel, iterations = 3)
	image, contours, hierarchy = cv2.findContours(g_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	minRect = None
	contourArea = 0
	for i in contours:
		rect = cv2.minAreaRect(i)
		area = rect[1][0]*rect[1][1]
		if area > contourArea and area > 200 :#\
		#and (rect[1][0] >= 2*rect[1][1] or 2*rect[1][0] <= rect[1][1]) :	# width >= 2*height
		#enable previous line on horizontal lines, not vertical
			minRect = rect
			contourArea = area
	g_new = np.zeros_like(g_res)
	if(contourArea != 0):
		box = cv2.boxPoints(minRect)
		box = np.int0(box)
		g_new = cv2.drawContours(g_new, [box], 0, (0,0,255), 3)

	cv2.imshow('frame',frame)
	cv2.imshow('new',g_new)
	cv2.imshow('green',g_res)

	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break

cap.release()
cv2.destroyAllWindows()


'''
This is some *beautiful* code that doesn't work and isn't really needed. I spent a lot of time on it.
			checked = frame[int(rect[0][0]):int(rect[0][0]+rect[1][0]), int(rect[0][1]):int(rect[0][1]+rect[1][1]) ]
			checked = cv2.cvtColor(checked, cv2.COLOR_BGR2GRAY)
			if(checked is not None):
				checker = np.ones(checked.shape, np.uint8)
				_, checked = cv2.threshold(checked, 5, 255, cv2.THRESH_BINARY)
				mask_chk = cv2.bitwise_and(checker, checked)
				print(cv2.countNonZero(mask_chk)/area)
'''
