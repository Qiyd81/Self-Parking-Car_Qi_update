# Import libaries
from multiprocessing import Process, Queue, Value, Lock, Array
import time   # Import time library for time control
import sys
import numpy as np
import cv2
from datetime import datetime
np.set_printoptions(threshold=sys.maxsize)

#Main: Step 1. Set Video Resolution Parameters
#Note: There will be less info to process if resolution decreases
x_res = 320 #640 #320 
y_res = 240 #480 #240 
center_x = x_res/2
center_y = y_res/2
#Main: Step 2. Create a VideoCapture object to capture video
cv2.namedWindow("preview")

videoCap = cv2.VideoCapture(0)
videoCap.set(3, x_res)
videoCap.set(4, y_res)
#Main: Step 3. Center Tolerance Parameters
tolerance = 10
red_threshold = 500000
#red_threshold =  100000

lower_red1 = np.array([0,50,50])
upper_red1 = np.array([10,255,255])
lower_red2 = np.array([170,50,50])
upper_red2 = np.array([180,255,255])
# Setting Kernel Convolution Parameters
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
frame = 0 
contours = 0
returnBoolean, frame = videoCap.read()


while True:
		# 1. Extract a frame from the video
    returnBoolean, frame = videoCap.read()
		# 2. Convert RGB color space to HSV (hue, saturation, value) color space
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		# Define range of red color in HSV
		# For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255].
		# H maps to 0-360 degree and S, V maps to 0-100%
		# 3. Threshold the HSV image to get only red colors
    mask1 = cv2.inRange(frame_hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(frame_hsv, lower_red2, upper_red2)
    mask= mask1 + mask2
		# 4. Check the sum of blue pixels, only try to send over for processing if greater than threshold
    sum_of_red = np.sum(mask)
    if (sum_of_red > red_threshold):
			#print(mask.shape)
			# 1. Implement the open and close operation to get rid of noise and solidify an object
        maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
			# 2. Extract contour
        contours,h=cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
        if (len(contours)>0):
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
       
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 0.5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), (0,0,255), 2)
               # cv2.putText("fire hydrant", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
    if frame is not None:   
        cv2.imshow("preview",frame) #Display Frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.2)
cv2.destroyAllWindows() 		#Turn off cv2 window
	