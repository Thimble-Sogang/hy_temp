import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
 
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("video.mp4")
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True )
    # lmList = detector.findPosition(img, draw=False)

    # topList, botList=detector.findFingerTipPosition(img,draw=False)
    # L_list=detector.findFingerTipLength(topList,botList)
    # C_list=detector.findFingerCenter(topList,botList)
    # S_list=detector.findFingerSlope(topList,botList,L_list)

    # detector.FingerPrintExpress(img,C_list,L_list,S_list)
    # cv2.imshow("FingerPrintArea", img)

    # # 거리로 판단하기
    # if detector.getDistance(lmList[8],lmList[0])<=detector.getDistance(lmList[7],lmList[0]):
    #     print("NO!!!")
    # else :
    #     print("YES!!!")
    # # 거리로 판단하기
    
     # 거리로 판단하기
    # if (detector.getDistance(lmList[8],lmList[7])+detector.getDistance(lmList[7],lmList[6])) >= detector.getDistance(lmList[8],lmList[6]):
    #     print("palmpalm")
    # else :
    #     print("back")
    # 거리로 판단하기


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break