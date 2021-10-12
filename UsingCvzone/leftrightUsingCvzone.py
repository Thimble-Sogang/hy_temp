from cvzone.HandTrackingModule import HandDetector
import cv2

# 블러 처리 여부 판단 (1이면 no blur, 0이면 blur)
def get_label(type,lmList):
    back = 0
    # 왼손 위
    if type=="Left" and (lmList[12][1] - lmList[0][1] < 0 ):
        if lmList[0][0] - lmList[2][0] >0 :
            back=0
        else :
            back=1
    # 왼손 아래
    elif type=="Left" and (lmList[12][1] - lmList[0][1] >= 0 ): 
        if lmList[0][0] - lmList[2][0] <0 :
            back=0
        else :
            back=1
    # 오른손 아래
    if type=="Right" and (lmList[12][1] - lmList[0][1] >= 0 ): 
        if lmList[17][0] - lmList[0][0] <0 :
            back=0
        else :
            back=1
    # 오른손 위
    elif type=="Right" and (lmList[12][1] - lmList[0][1] < 0 ): 
        if lmList[17][0] - lmList[0][0] <0 :
            back=1
        else :
            back=0

    print(back)
    return back



cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # 손이 1개 일 경우
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # 21개 랜드마크
        bbox1 = hand1["bbox"]  # x,y,w,h로 손 아웃라인 박스 좌표
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right
        
        # 블러처리 판단함수 
        get_label(handType1,lmList1)

        if len(hands) == 2:
            # 손이 2개일 경우
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # 21개 랜드마크
            bbox2 = hand2["bbox"]  # x,y,w,h로 손 아웃라인 박스 좌표
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"
            
           # 블러처리 판단함수 
            get_label(handType2,lmList2)
            
            fingers2 = detector.fingersUp(hand2)

            # Find Distance between two Landmarks. Could be same hand or different hands
            length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
    # Display
    img = cv2.flip(img, 1)

    
    cv2.imshow("Image", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()