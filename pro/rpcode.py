from picamera.array import PiRGBArray
from picamera import PiCamera
from RBConnection import RBConnection
import cv2
import numpy as np
import re

#extract data from the input file
f = open('/home/pi/Desktop/lights/sg_1/pro/input.txt',"r")
lines = f.readlines()
results = re.findall('=([\d.]+)',lines[0])
results2 = re.findall('=([\d.]+)',lines[2])
config=map(float,results)


#assign extracted values for each variables
[resX,resY,frameRate,minThresh,maxTresh,minArea,maxArea]=[  int(config[0]),int(config[1]),float(config[2]),float(config[3]), float(config[4]),float(config[5]),float(config[6])]
[minCir,minConv,minInert,LR,Move_low,Move_high]=[float(config[7]),float(config[8]),float(config[9]),float(config[10]),float(config[11]),float(config[12]) ]
[X_low,X_high,Y_low,Y_high,keyA,ID,check,port]=[ int(config[13]),int(config[14]),int(config[15]),int(config[16]),int(config[17]),int(config[18]),int(config[19]),int(config[20])]
IP=results2[0]

#connection
con = RBConnection('ID', IP, port)

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

counter_prev =0
movement_prev=0
counter_check=0

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	counter =0
	movement=0
	frame = f.array
	image = fgbg.apply(frame,learningRate=LR)	
	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        
	#detecting the centroids of the blobs
	points = detector.detect(image)

	#drawing circles on keypoints 
        if keyA:
		image_with_blobs = cv2.drawKeypoints(frame, points, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
	#for movement
	(cnts,_) = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#calculations for counting
	for kp in points :
        	x=round(kp.pt[0])
        	y=round(kp.pt[1])
        	if (X_low<x<X_high and Y_low<y<Y_high):
            		if not points is None:
				counter+=1
	
	#calculations for movement
	for c in cnts:
		area=cv2.contourArea(c)
		if Move_low<area<Move_high:
			movement+=1

	#counter check
	if(counter_prev==counter):
		counter_check+=1
	else:
		counter_check=0	

	#send
	try:
		if (counter!=counter_prev) or (counter_check>check):
			con.send({'sensor': ID, 'activity': movement,'Roger':counter})	
			if (counter_check>check):
				counter_check=0

	#if server down, I will try to connect again
	except:
		con = RBConnection('ID',IP, port)

	#display the values
	if keyA:
	    	print "CountB=%d" %counter
		print "Move=%d" %movement   
 	
	#drawing a rectangle over the interested area <---remove this after tunning
	if keyA:
		cv2.rectangle(image_with_blobs,(X_low,Y_low),(X_high,Y_high),(255,0,0),1)
		cv2.rectangle(image,(X_low,Y_low),(X_high,Y_high),(255,0,0),1)	
		
	#display the image with blobs
	if keyA:
		cv2.imshow("frame", image)

	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
