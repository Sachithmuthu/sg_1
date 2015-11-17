from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import re

f = open('input.txt',"r")
lines = f.readlines()
results = re.findall('=([\d.]+)',lines[0])
config=map(float,results)

[resX,resY,frameRate,minThresh,maxTresh,minArea,maxArea]=[  int(config[0]),int(config[1]),float(config[2]),float(config[3]), float(config[4]),float(config[5]),float(config[6])]
[minCir,minConv,minInert,LR,threshMove,threshCount]=[float(config[7]),float(config[8]),float(config[9]),float(config[10]),float(config[11]),float(config[12]) ]

camera = PiCamera()
camera.resolution = (resX,resY)				
camera.framerate = frameRate							
rawCapture = PiRGBArray(camera, size= (resX,resY) )

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
fgbg = cv2.BackgroundSubtractorMOG2()

params = cv2.SimpleBlobDetector_Params()

params.minThreshold = minThresh						
params.maxThreshold =maxTresh 					

params.filterByArea = True
params.minArea = minArea							
params.maxArea = maxArea							
	
params.filterByCircularity = False
params.minCircularity = minCir						

params.filterByConvexity = False
params.minConvexity =minConv 						

params.filterByInertia = False
params.minInertiaRatio =minInert 					

params.filterByColor=False

ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	counter =0
	move=0

        frame = f.array
	image = fgbg.apply(frame,learningRate=LR)	
	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        points = detector.detect(image) 
        image_with_blobs = cv2.drawKeypoints(image, points, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        for kp in points :
	    diameter=round(kp.size)
	    if diameter>threshMove:  								
	    	move+=1
	    if diameter>threshCount:								
		counter+=1
	x=move*5
	movement=min(x,100)
	print "Count=%d" %counter,
	print "Move=%d" %movement,
        print      
 
	cv2.imshow("frame", image_with_blobs )
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)
