import cv2
import mediapipe as mp
import numpy as np

shoe_img = cv2.imread("shoe.png", cv2.IMREAD_UNCHANGED)

if shoe_img is None:  


    print("Error: Could not load shoe image. Check the file path!")
    exit()

print("Shoe image loaded successfully!")

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = pose.process(rgb_frame)

    if result.pose_landmarks:
        h, w, _ = frame.shape 

        right_foot = result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]

  
        shoe_x, shoe_y = int(right_foot.x * w) - 75, int(right_foot.y * h) - 75  

        shoe_resized = cv2.resize(shoe_img, (150, 150), interpolation=cv2.INTER_AREA)  

        sh, sw, sc = shoe_resized.shape
        if sc == 4: 
            alpha_channel = shoe_resized[:, :, 3] / 255.0  
            shoe_rgb = shoe_resized[:, :, :3]  

            shoe_x = max(0, min(shoe_x, w - sw))
            shoe_y = max(0, min(shoe_y, h - sh))


            roi = frame[shoe_y:shoe_y + sh, shoe_x:shoe_x + sw]

    
            for c in range(3):  
                roi[:, :, c] = (1 - alpha_channel) * roi[:, :, c] + alpha_channel * shoe_rgb[:, :, c]

            frame[shoe_y:shoe_y + sh, shoe_x:shoe_x + sw] = roi  

    cv2.imshow("Virtual Shoe Try-On", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()