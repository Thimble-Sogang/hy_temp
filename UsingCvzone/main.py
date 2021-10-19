from cvzone.HandTrackingModule import HandDetector
import cv2
import math

def get_label(type,lmList):
    back = 0
    # 왼손 위
    if type=="Left" and (lmList[12][1] - lmList[0][1] < 0 ):
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("back ->")
                back = 1
            else:
                print("front ->")
        else :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("back <-")
                back = 1
            else:
                print("front <-")
    # 왼손 아래
    elif type=="Left" and (lmList[12][1] - lmList[0][1] >= 0 ):
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("front ->")
            else:
                print("back ->")
                back = 1
        else :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("front <-")
            else:
                print("back <-")
                back = 1
    # 오른손 아래
    if type=="Right" and (lmList[12][1] - lmList[0][1] >= 0 ): 
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("back ->")
                back = 1
            else:
                print("front ->")
        else :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("back <-")
                back = 1
            else:
                print("front <-")
    # 오른손 위
    elif type=="Right" and (lmList[12][1] - lmList[0][1] < 0 ): 
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("front ->")
            else:
                print("back ->")
                back = 1
        else :
            if(lmList[5][0]-lmList[9][0]>=0):
                print("front <-")
            else:
                print("back <-")
                back = 1

    return back


def findFingerTipLength(toplist, botList):
            #return legnth of finger tip point
        L_list=[]
        for i in range(len(toplist)):
                x=toplist[i][0]-botList[i][0]
                y=toplist[i][1]-botList[i][1]
                L_list.append(math.sqrt(x*x + y*y))
        return L_list

def findFingerCenter(toplist,botList):
    #return finger center point list
    C_list=[]
    for i in range(len(toplist)):
        C_list.append([(toplist[i][0]+botList[i][0])/2,(toplist[i][1]+botList[i][1])/2])
    return  C_list

def findFingerSlope(topList,botList,L_list):
    S_list=[]
    for i in range(len(topList)):
        #print(L_list[i])
        #print(botList[i][1]-topList[i][1])
        rad=math.acos((topList[i][0]-botList[i][0])/L_list[i])
        #rad->degree
        slope=rad*180/math.pi

        if topList[i][1]>=botList[i][1]: #손가락 아래쪽
            slope=slope-180
        else: #손가락 위쪽
            #if topList[i][0]>botList[i][0]:
                slope = 180 - slope

        # print(slope)
        S_list.append(slope)
    return S_list

def FingerPrintExpress(img,C_list,L_list,S_list):
    for i in range(len(C_list)):
        cx=C_list[i][0]
        cy=C_list[i][1]
        cv2.ellipse(img,(int(cx),int(cy)),(int(L_list[i]/2),int(L_list[i]/4)),S_list[i],startAngle=0,endAngle=360,color=(0,0,0),thickness=-1)


def findFingerTipPosition(img,lmList):
    topList=[]
    botList=[]
    for id, lm in enumerate(lmList):
        cx, cy = int(lm[0]), int(lm[1])
        if(id==3 or id==7 or id==11 or id==15 or id==19):
            botList.append([cx,cy])
            cv2.circle(img, (cx, cy), 3, (0, 0, 0), cv2.FILLED)
        elif(id==4 or id==8 or id==12 or id==16 or id==20):
            topList.append([cx,cy])
            cv2.circle(img, (cx, cy), 1, (0, 0, 0), cv2.FILLED)
    return topList,botList


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    if hands:
        # 손이 1개 일 경우
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # 21개 랜드마크
        bbox1 = hand1["bbox"]  # x,y,w,h로 손 아웃라인 박스 좌표
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right
        
        # 블러처리 판단함수 
        get_label(handType1,lmList1)

        # 지문 블러처리
        if get_label(handType1,lmList1) == 0:
            topList, botList = findFingerTipPosition(img,lmList1)
            L_list=findFingerTipLength(topList,botList)
            C_list=findFingerCenter(topList,botList)
            S_list=findFingerSlope(topList,botList,L_list)
            FingerPrintExpress(img,C_list,L_list,S_list)

        if len(hands) == 2:
            # 손이 2개일 경우
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # 21개 랜드마크
            bbox2 = hand2["bbox"]  # x,y,w,h로 손 아웃라인 박스 좌표
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"

           # 블러처리 판단함수 
            # get_label(handType2,lmList2)
        
            # 지문 블러처리
            if get_label(handType2,lmList2) == 0:
                topList, botList = findFingerTipPosition(img,lmList2)
                L_list=findFingerTipLength(topList,botList)
                C_list=findFingerCenter(topList,botList)
                S_list=findFingerSlope(topList,botList,L_list)
                FingerPrintExpress(img,C_list,L_list,S_list)


    # Display
    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()