from matplotlib import pyplot as plt
import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

joint_list = [[8,7,6], [12,11,10], [16,15,14], [20,19,18]]

def get_label(index, hand, results):
    back = 0
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))
            # 중지 - 손목 : 양수면 아래방향, 음수면 위
            # idx 0 왼손 / 1 오른손
            
            # 왼손 위
            if idx==0 and (hand.landmark[12].y - hand.landmark[0].y < 0 ):
                if hand.landmark[17].x - hand.landmark[0].x <0 :
                    back=0
                else :
                    back=1
            # 왼손 아래
            elif idx==0 and (hand.landmark[12].y - hand.landmark[0].y >= 0 ): 
                if hand.landmark[17].x - hand.landmark[0].x >=0 :
                    back=0
                else :
                    back=1
            # 오른손 아래
            if idx==1 and (hand.landmark[12].y - hand.landmark[0].y >= 0 ): 
                if hand.landmark[17].x - hand.landmark[0].x <0 :
                    back=0
                else :
                    back=1
            # 오른손 위
            elif idx==1 and (hand.landmark[12].y - hand.landmark[0].y < 0 ): 
                if hand.landmark[17].x - hand.landmark[0].x <0 :
                    back=1
                else :
                    back=0
            
            # # Extract Coordinates
            # coords = tuple(np.multiply(
            #     np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
            # [640,480]).astype(int))
            
    return back



def draw_finger_angles(image, results, joint_list):
    
    # Loop through hands
    for hand in results.multi_hand_landmarks:
        #Loop through joint sets 
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y]) # First coord
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y]) # Second coord
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y]) # Third coord
            
            radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            
            if angle > 180.0:
                angle = 360-angle
                
            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened():
        ret, frame = cap.read()
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        image = cv2.flip(image, 1)
        
        # Set flag
        image.flags.writeable = False
        
        # Detections
        results = hands.process(image)
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Detections
        # print(results)
        
        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                         )
                
                # Render left or right detection
                back = get_label(num, hand, results)
                if back :
                  print("NONONONONONO")
                else :
                  print("YYYYYYYYYYYYY")
                   

            
            # Draw angles to image from joint list
            draw_finger_angles(image, results, joint_list)
            
        # Save our image    
        #cv2.imwrite(os.path.join('Output Images', '{}.jpg'.format(uuid.uuid1())), image)
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()