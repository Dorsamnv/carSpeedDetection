import cv2

cap = cv2.VideoCapture("C:\\Users\\Royal Center\\Downloads\\27260-362770008_medium.mp4")
if not cap.isOpened():
    print("error: unable to load the video")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
print("frame rate:", fps)
cap.release()