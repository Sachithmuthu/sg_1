import numpy as np
import cv2

cap = cv2.VideoCapture(0)    #'Vehicle Counting.mp4' 'People Counter With OPENCV.mp4'

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
fgbg = cv2.createBackgroundSubtractorMOG2(0,0,False)

params = cv2.SimpleBlobDetector_Params()

#params.minThreshold = 10;
#params.maxThreshold = 255;

params.filterByArea = True
params.minArea = 4700
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

while(1):
    counter =0
    ret, frame = cap.read()

    image = fgbg.apply(frame)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    image = cv2.GaussianBlur(image,(7,7),3)
    image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,3,1)
    #ret,image = cv2.threshold(image,10,255,cv2.THRESH_BINARY)
    
    #>>>>>>>>>>>>ostu's
    #image = cv2.GaussianBlur(image,(7,7),0)
    #ret,image= cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #image = cv2.bilateralFilter(image,9,175,175)
    #image = cv2.GaussianBlur(image,(7,7),3)
    #image = cv2.Laplacian(image,cv2.CV_64F)
    #image = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=5)
    #image = cv2.Sobel(image,cv2.CV_64F,0,1,ksize=5)
    #image = cv2.Laplacian(image,depth,ksize = kernel_size,scale = scale,delta = delta)

    # Detect blobs
    points = detector.detect(image)
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    blob_image = cv2.drawKeypoints(frame, points, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    #print the values----------------------------------------------------------------------------------------------------------------
    for kp in points :
        if not points is None:
            counter+=1
    print "Count=%d" %counter,

    for kp in points :
        print "[x=%d,y=%d]" %(round(kp.pt[0]),round(kp.pt[1])),
    print       
    #--------------------------------------------------------------------------------------------------------------------------------    
    #cv2.imshow('frame',image)
    cv2.imshow('frame',blob_image)

    if cv2.waitKey(1) & 0xFF == ord('z'):
        break

cap.release()
cv2.destroyAllWindows()