import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
 
 
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True )
    # lmList = detector.findPosition(img, draw=False)

    # # findFingerTipPosition은 손이 감지 되지 않으면 에러가 발생합니다.
    # topList, botList=detector.findFingerTipPosition(img,draw=False)

    # L_list=detector.findFingerTipLength(topList,botList)
    # C_list=detector.findFingerCenter(topList,botList)
    # S_list=detector.findFingerSlope(topList,botList,L_list)

    # detector.FingerPrintExpress(img,C_list,L_list,S_list)
    img = cv2.flip(img,1)
    cv2.imshow("Image", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break