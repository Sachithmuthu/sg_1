import numpy as np
import cv2
import time

def gamma_correction(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    return np.uint8(img*255)

cap = cv2.VideoCapture(0) #'Image Processing Vehicle Counting Using OpenCV.mp4'
time.sleep(2)
ret, frame = cap.read()

#process the ref img
gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imwrite("test_image.jpg", gray1)
gam = gamma_correction(gray1, 0.5)
clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(8,8))
dst = clahe.apply(gam)
cv2.imwrite("file.jpg", dst)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #making gray img
    gam2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(8,8))
    gray = clahe.apply(gam2)

    #sutracting the frame from the ref img
    subarray=cv2.absdiff(gray,dst)

    #thresholding the processed image
    ret,th = cv2.threshold(subarray,100,255,cv2.THRESH_BINARY)

    #Display the resulting frame
    cv2.imshow('frame',th)

    #counting the number of white pix
    pix = cv2.countNonZero(th)

    #divide by the avg area of a human
    num = pix/5000
    print('The number of people: ' + str(num))	
   
    if cv2.waitKey(1) & 0xFF == ord('z'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

