import cv2

#print("Before URL")
cap = cv2.VideoCapture(0)
#print("After URL")

while True:
  # Capture frame-by-frame
    ret, frame = cap.read()
    #print cap.isOpened(), ret
    if frame is not None:
        # Display the resulting frame
        cv2.imshow('frame',frame)
        # Press q to close the video windows before it ends if you want
        if cv2.waitKey(22) & 0xFF == ord('q'):
            break
    else:
        print ("Frame is None")
cap.release()
cv2.destroyAllWindows()