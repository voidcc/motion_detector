#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
"""

import argparse
import datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the video file")
ap.add_argument("-a", "--min_area", type = int, default = 500, 
	help = "minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
else:
	camera = cv2.VideoCapture(args['video'])

firstFrame = None

while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	grabbed, frame = camera.read()
	text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the 
	# end of the video.
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, 500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	#cv2.imshow('frame', gray)

	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and 
	# the first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	#cv2.imshow('frame', frameDelta)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations = 2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
		cv2.CHAIN_APPROX_SIMPLE)
	
	# loop over the contours
	for c in cnts:
		#if thr contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw iton the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S %p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# show the frame and record
	cv2.imshow("Security Feed", frame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)

	# if the 'q' key is pressed, break from the loop
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

camera.release()
cv2.destroyAllWindows()