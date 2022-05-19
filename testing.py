# import the necessary packages
import tensorflow as tf
from imutils.video import VideoStream
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import time
import timestamp
import cv2
import os
#from datetime import datetime
import serial

#arduino = serial.Serial('COM4', 9600, timeout=.1)
#time.sleep(1)
print("[INFO] Loading the Model...")
model=load_model('neural.model')
#arduino.write(b'ready')

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(5.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 600 pixels
	frame = vs.read()
	if frame is None:
            logging.warning("Empty Frame")
            time.sleep(0.1)
            count+=1
            if count < 3:
                continue
            else: 
              break
            print(frame.shape)
	frame = imutils.resize(frame, width=600)

	import datetime
	now = datetime.datetime.now()
	print ("Current date and time : ")
	print (now.strftime("%Y-%m-%d %H:%M:%S"))
	ts = now.strftime("%A %d %B %Y %I:%M:%S %p")

	image = frame
        
	image = cv2.resize(image, (28, 28))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	# classify the input image
	(nonbio, bio) = model.predict(image)[0]
	# build the label
	label = "Biodegradable" if bio > nonbio else "Non-Biodegradable"
	y=label
	print(y)
	org = (15, 20)
	# show the label of predicted input
	cv2.putText(frame,y,org,cv2.FONT_HERSHEY_SIMPLEX,0.70,(0,0,255),2)
	# show the output frame and wait for a key press
	cv2.putText(frame, ts, (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX,0.70, (255, 100, 20), 2)
	cv2.imshow("Frame", frame)
	time.sleep(2.0)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
print("[INFO] Video Stream Ended...")

