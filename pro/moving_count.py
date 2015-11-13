import numpy as np
import cv2
import time

def gamma_correction(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    return np.uint8(img*255)

cap = cv2.VideoCapture('Vehicle Counting.mp4')

sub = cv2.createBackgroundSubtractorMOG2()

while(True):
	#capture frame-by-frame
    ret, frame = cap.read()

    #framing
    dst = sub.apply(frame,0.1)

    #counting the number of white pix
    pix = cv2.countNonZero(dst)

    #divide by the avg area of a human <---change the avg value(5000)
    num = pix/5000
    print('Number of people: ' + str(num))	

    cv2.imshow('frame',dst)
    
    if cv2.waitKey(1) & 0xFF == ord('z'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()