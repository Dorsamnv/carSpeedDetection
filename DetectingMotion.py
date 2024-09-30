
import cv2

video_path = "C:\\Users\\Royal Center\\Downloads\\VID_20240824_195729_210.mp4"
cap = cv2.VideoCapture(video_path)
backSub = cv2.createBackgroundSubtractorMOG2()
while True:
  ret, frame = cap.read()
  if not ret :
    break
  fgMask = backSub.apply(frame)
  contours,_ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    min_area = 1000
    if cv2.contourArea(contour) > min_area:
        cv2.rectangle(frame, (x,y) , (x+w, y+h), (0,255,0), 2)
  cv2.imshow("Motion Detection", frame)
  if cv2.waitKey(1) & 0xFF== ord('q'):
     break
cap.release()
cv2.destroyAllWindows()

  
