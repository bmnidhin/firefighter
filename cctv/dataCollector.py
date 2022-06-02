import cv2
import numpy as np
import os
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
#cap = cv2.VideoCapture('./videos/housefire.mp4')
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
counter = 0
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    # Display the resulting frame
    directory = r'D:\Nidhin_Projects\raspi\firefighter\cctv\frames'
    os.chdir(directory)
    cv2.imshow('Frame',frame)
    if counter %1 == 0:
        cv2.imwrite('frame'+str(counter)+'.jpg',frame)
    counter += 1
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()