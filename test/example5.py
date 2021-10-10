import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import numpy as np
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("video.mp4")
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True )
    
      # 케니 엣지 적용 
    edges = cv2.Canny(img,100,200)

    # 결과 출력
    cv2.imshow('Original', img)
    cv2.imshow('Canny', edges)

    # cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break