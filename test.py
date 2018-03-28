import threading
import cv2
import sys
import os
import obd
import time

time.sleep(0.1)
realdev = os.readlink("/dev/ttySim")
connection = obd.OBD(realdev)
cmd = obd.commands.SPEED
red,green,blue = 0,255,0
red2,green2,blue2 = 0,255,0
flag,flag2 = 0,0
set = 0
car_cascade = cv2.CascadeClassifier('lbp_carcascade.xml')
cam = cv2.VideoCapture(1)
#cam.set(3,640)
#cam.set(4,480)
while True:
    response = connection.query(cmd)
    speed = response.value
    ret_val, img = cam.read()
    #cv2.transpose(img, img)
    #cv2.flip(img, img, -1);
    cropped = img[200:400, 0:640]
    gray = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
    split_speed = str(speed).split(" ") 
    cars = car_cascade.detectMultiScale(gray,
					scaleFactor = 1.2,
					minNeighbors = 5,
					minSize =(50,50))
    if len(cars) != 0:
    	print "Found "+str(len(cars))+" car(s)"
    for (x,y,w,h) in cars:
   	if x >= 100 and x <= 320:
		#cv2.rectangle(cropped,(x,y),(x+w,y+h),(255,0,0),1)
		if y+h <= 200*5/6 and y+h > 200*4/6 :
			red = 255
			green = 255
			blue = 0
		elif y+h > 200*5/6:
			red = 255
			green=0 
			blue = 0
			flag = 1
		else:
	  		green = 255
	  		red = 0
          		blue = 0
			flag = 0
	elif x > 320 and x <= 520:
		if y+h <= 200*5/6 and y+h > 200*4/6 :
            		red2 = 255
            		green2 = 255
           		blue2 = 0
        	elif y+h > 200*5/6:
            		red2 = 255
            		green2=0 
            		blue2 = 0
			flag2 = 1
        	else:
            		green2 = 255
            		red2 = 0
            		blue2 = 0
			flag2 = 0
    if flag == 0 and flag2 == 0:
	set = 0
    if int(split_speed[0]) >= 20:
	if (flag or flag2) and set == 0:
		print "Activated"
		set = 1
		os.system("mpg321 ding.wav") 
    cv2.line(cropped,(0,200),(213,100),(blue,green,red),1)
    cv2.line(cropped,(640,200),(426,100),(blue2,green2,red2),1)
    cv2.imshow('Video', cropped)
    if cv2.waitKey(1) == 27: 
        break  # esc to quit
cv2.destroyAllWindows()

