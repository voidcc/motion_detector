#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import imutils
import time
import cv2
import os

frame_1 = None
frame_2 = None
motion_num = 0
min_area = 1000

clicked = False

def onMouse(event, x, y, flags, param):
	global clicked
	if event == cv2.cv.CV_EVENT_LBUTTONUP:
		clicked = True

camera = cv2.VideoCapture(0)
#time.sleep(0.25)
cv2.namedWindow('MyWindow')
cv2.setMouseCallback('MyWindow', onMouse)

while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text

	(grabbed, frame) = camera.read()

	if not grabbed:
		time.sleep(0.25)
		continue

	#cv2.imshow('MyWindow', frame)
	#frame = imutils.resize(frame, 500)
	frame_2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame_2 = cv2.GaussianBlur(frame_2, (21, 21), 0)

	if frame_1 is None:
		frame_1 = frame_2
		continue

	frameDelta = cv2.absdiff(frame_1, frame_2)
	#cv2.imshow('frame', frameDelta)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	#cv2.imshow("frame_1", frame_1)
	#cv2.imshow("frame_2", frame_2)
	thresh = cv2.dilate(thresh, None, iterations = 2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
		cv2.CHAIN_APPROX_SIMPLE)

	motion_num = 0

	for c in cnts:
		#if thr contour is too small, ignore it
		if cv2.contourArea(c) < min_area:
			continue
		motion_num += 1
		# compute the bounding box for the contour, draw iton the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.putText(frame, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	cv2.imshow("MyWindow", frame)
	print "motion_num", motion_num, datetime.datetime.now()

	frame_1 = frame_2.copy()
	#time.sleep(0.2)

	if cv2.waitKey(1) != -1 or clicked:
		break

camera.release()
cv2.destroyAllWindows()