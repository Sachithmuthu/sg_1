from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

[[float(i) for i in line.strip().split(',')]for line in open('input.txt').readlines()]
reading=line.strip()
config=reading.split(',')
 
camera = PiCamera()
camera.resolution = (int(config[0]),int(config[1]))				#(480,360)
camera.framerate = float(config[2])							#15
rawCapture = PiRGBArray(camera, size= (float(config[0]),float(config[1])) )

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
fgbg = cv2.BackgroundSubtractorMOG2()

params = cv2.SimpleBlobDetector_Params()

params.minThreshold = float(config[3]) 						#10	
params.maxThreshold = float(config[4]) 						#255

params.filterByArea = True
params.minArea = float(config[5]) 							#700
params.maxArea = float(config[6]) 							#1000  
	
params.filterByCircularity = False
params.minCircularity = float(config[7]) 						#0.2

params.filterByConvexity = False
params.minConvexity =float(config[8]) 						#0.87

params.filterByInertia = False
params.minInertiaRatio =float(config[9]) 					#0.01

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
	image = fgbg.apply(frame,learningRate=float(config[10]))	#0.02
	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        points = detector.detect(image) 
        image_with_blobs = cv2.drawKeypoints(image, points, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        for kp in points :
	    d=round(kp.size)
	    if d>float(config[11]):  								#6
	    	move+=1
	    if d>float(config[12]):								#30
		counter+=1
	x=move*5
	movement=min(x,100)
	print "Count=%d" %counter,
	print "Move=%d" %movement,
        print      
 
	cv2.imshow("frame", image_with_blobs )
	key = cv2.waitKey(1) & 0xFF
 
	rawCapture.truncate(0)
