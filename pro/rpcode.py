from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import re

#extract data from the input file
f = open('input.txt',"r")
lines = f.readlines()
results = re.findall('=([\d.]+)',lines[0])
config=map(float,results)

#assign extracted values for each variables
[resX,resY,frameRate,minThresh,maxTresh,minArea,maxArea]=[  int(config[0]),int(config[1]),float(config[2]),float(config[3]), float(config[4]),float(config[5]),float(config[6])]
[minCir,minConv,minInert,LR,threshMove,threshCount]=[float(config[7]),float(config[8]),float(config[9]),float(config[10]),float(config[11]),float(config[12]) ]
[X_low,X_high,Y_low,Y_high]=[ int(config[13]),int(config[14]),int(config[15]),int(config[16])]

#camera configuration
camera = PiCamera()
camera.resolution = (resX,resY)				
camera.framerate = frameRate							
rawCapture = PiRGBArray(camera, size= (resX,resY) )

#image filtering
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
#background substraction
fgbg = cv2.BackgroundSubtractorMOG2()

#set up parameters for blob detection
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
	counterB=0
	frame = f.array
	image = fgbg.apply(frame,learningRate=LR)	
	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        
	#detecting the centroids of the blobs
	points = detector.detect(image)

	#drawing circles on keypoints 
        image_with_blobs = cv2.drawKeypoints(frame, points, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
	#calculations
	for kp in points :
        	x=round(kp.pt[0])
        	y=round(kp.pt[1])
		diameter=round(kp.size)
        	if (X_low<x<X_high and Y_low<y<Y_high and diameter>threshCount ):
            		counterB+=1
		if diameter>threshMove:  								
	    		move+=1
       		print "[x=%d,y=%d]" %(x,y),
	movement=min(move,100)
    	
	#display the values
	print "CountB=%d" %counterB,
	print "Move=%d" %movement,
        print      
 
	#display the image with blobs
	cv2.imshow("frame", image_with_blobs )
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)
