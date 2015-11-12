from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imutils
 
camera = PiCamera()
camera.resolution = (150, 100)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(150, 100))

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
fgbg = cv2.BackgroundSubtractorMOG2()

params = cv2.SimpleBlobDetector_Params()

#params.minThreshold = 10;
#params.maxThreshold = 255;

params.filterByArea = True
params.minArea = 700
#params.maxArea = 1000    <<<<<<<<<<<<<<<<<--------------------------set this value as well!!!

params.filterByCircularity = False
params.minCircularity = 0.2

params.filterByConvexity = False
params.minConvexity = 0.87

params.filterByInertia = False
params.minInertiaRatio = 0.01

#setting up the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	counter =0

        frame = f.array
	#frame = imutils.resize(frame, width=500)
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	image = fgbg.apply(frame)	

	image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        image = cv2.GaussianBlur(image,(3,3),3)
        image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,3,1)
 

	# Detect blobs
        points = detector.detect(image)
        #cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob    
        blob_image = cv2.drawKeypoints(frame, points, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        #print the values----------------------------------------------------------------------------------------------------------------
        for kp in points :
            if not points is None:
                counter+=1
        print "Count=%d" %counter,

        #for kp in points :
          #  print "[x=%d,y=%d]" %(round(kp.pt[0]),round(kp.pt[1])),
        print       

        #-------------------------------------------------------------------------------------------------------------------------------- 
 
	# show the frame
	cv2.imshow("frame", blob_image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	#if key == ord("z"):
	#	break

