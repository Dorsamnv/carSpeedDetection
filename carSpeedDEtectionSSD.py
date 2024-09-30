import cv2
import torch 
import torchvision
import math
 #hi
model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(pretrained=True)
model.eval()

confidence_threshold = 0.5
frame_rate = 29.97002997002997 
ppm = 8.8
speed_limit = 50
fine_amount = 25

def estimate_speed(location1, location2, ppm, fps):
    d_pixels = math.sqrt((location2[0]-location1[0])**2 + (location2[1]-location1[1])**2)
    d_meter = d_pixels/ppm
    speed = d_meter * fps * 3.6
    return speed
def detect_cars(frame, frame_rate, ppm):
    global pos_list_prev
    img_tensor = torchvision.transforms.ToTensor()(frame)
    with torch.no_grad():
        predictions = model([img_tensor])
    for pred, score in zip(predictions[0]["boxes"], predictions[0]["scores"]):
        x1,y1,x2,y2 = map(int, pred)
        if score >= confidence_threshold:
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            centorid_x = (x1 + x2) / 2
            centorid_y = (y1 + y2) / 2
            pos_list = [centorid_x, centorid_y]
            if pos_list_prev is not None:
                speed = estimate_speed(pos_list_prev, pos_list, ppm, frame_rate)
                if speed >= speed_limit :
                    issue_speeding_ticket(speed)
                    print("Speeding Ticket Isssued")
            else:
                speed = 0
            cv2.putText(frame, f'Speed: {speed: .2f} km/h', (x1,y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,2), 1)
            pos_list_prev = pos_list
    return frame

def issue_speeding_ticket(speed):
     filename = "speeding_ticket.txt"
     with open(filename, "a") as file:
        file.write("speeding ticket!\n")
        file.write(f"detected speed: {speed:.2f} km/h\n")
        file.write(f"fine amount: ${fine_amount}\n")
        file.write("\n")
    
cap = cv2.VideoCapture("C:\\Users\\Royal Center\\Downloads\\27260-362770008_medium.mp4")
if not cap.isOpened():
    print('error: The video is unavailable')
    exit()
pos_list_prev = None
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    processed_frame= detect_cars(frame, frame_rate, ppm)
    cv2.imshow("frame", processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
