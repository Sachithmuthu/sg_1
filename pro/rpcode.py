from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imutils
 
camera = PiCamera()
camera.resolution = (480,360)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(480,360))

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
fgbg = cv2.BackgroundSubtractorMOG2()


##########################################           CONFIG
params = cv2.SimpleBlobDetector_Params()

params.minThreshold = 10;
params.maxThreshold = 255;

params.filterByArea = True
params.minArea = 700
#params.maxArea = 1000    <<<<<<<<<<<<<<<<<--------------------------set this value as well!!!

params.filterByCircularity = False
params.minCircularity = 0.2

params.filterByConvexity = False
params.minConvexity = 0.87

params.filterByInertia = False
params.minInertiaRatio = 0.01

params.filterByColor=False

#setting up the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	counter =0
	move=0

        frame = f.array
	#image = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,3,1)
	#ret,image = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
	image = fgbg.apply(frame,learningRate=0.02)	
	
	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
	#ret,image = cv2.threshold(image,150,255,cv2.THRESH_BINARY)
        #image = cv2.GaussianBlur(image,(3,3),3)
        #image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,3,1)
	#ret,image = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#
 

	# Detect blobs
        points = detector.detect(image)
        #cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob    
        blob_image = cv2.drawKeypoints(image, points, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        #print the values----------------------------------------------------------------------------------------------------------------
        #for kp in points :
            #if not points is None:
                #counter+=1
        #print "Count=%d" %counter,

        for kp in points :
           # print "%d" %(round(kp.size)),
	    d=round(kp.size)
	    if d>6:
	    	move+=1
	    if d>30:
		counter+=1
	x=move*5
	movement=min(x,100)
	print "Count=%d" %counter,
	print "Move=%d" %movement,
        print      
	


        #-------------------------------------------------------------------------------------------------------------------------------- 
 
	# show the frame
	cv2.imshow("frame", blob_image  )
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	#if key == ord("z"):
	#	break

