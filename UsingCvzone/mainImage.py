from cvzone.HandTrackingModule import HandDetector
import cv2
import math
import numpy as np
import os
import csv

# 내부 함수
def getAngle(lmList):
    x1 = lmList[1][0] - lmList[0][0]
    y1 = lmList[1][1] - lmList[0][1]
    x2 = lmList[17][0] - lmList[0][0]
    y2 = lmList[17][1] - lmList[0][1]
    rad = math.acos((x1*x2 + y1*y2) / (getDistance(lmList[1],lmList[0]) * getDistance(lmList[17],lmList[0])))
    slope=rad*180/math.pi
    return slope

def get_label(type,lmList):
    back = 1
    below = 0
    angle = getAngle(lmList)
    # 왼손 위
    if type=="Left" and (lmList[12][1] - lmList[0][1] < 0 ):      
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=-0): # 손이 11시 or 1시 방향인지 check
                back = 1
            else:
                if angle < 70 and angle > 100 :
                    back=1
                else:
                    back = 0
        else :
            if(lmList[5][0]-lmList[9][0]>=-0):
                back = 1
            else:
                if angle < 70 and angle > 100 :
                    back=1
                else:
                    back = 0
    # 왼손 아래
    elif type=="Left" and (lmList[12][1] - lmList[0][1] >= 0 ):
        below = 1
        angle = 180 - angle
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=0):
                if angle < 70 or angle > 100 :
                    back=1
                else:
                    back = 0
            else:
                back = 1
        else :
            if(lmList[5][0]-lmList[9][0]>=0):
                if angle < 70 or angle > 100 :
                    back=1
                else:
                    back = 0
            else:
                back = 1
    # 오른손 아래
    if type=="Right" and (lmList[12][1] - lmList[0][1] >= 0 ):
        below=1
        angle = 180- angle
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=-0):
                back = 1
            else:
                if angle < 70 or angle > 100 :
                    back=1
                else:
                    back = 0
        else :
            if(lmList[5][0]-lmList[9][0]>=-0):
                back = 1
            else:
                if angle < 70 or angle > 100 :
                    back=1
                else:
                    back = 0
    # 오른손 위
    elif type=="Right" and (lmList[12][1] - lmList[0][1] < 0 ): 
        if ((lmList[9][0]+lmList[13][0])/2 - lmList[0][0] <= 0) :
            if(lmList[5][0]-lmList[9][0]>=0):
                if angle < 70 or angle > 100 :
                    back=1
                else:
                    back = 0
            else:
                back = 1
        else :
            if(lmList[5][0]-lmList[9][0]>=0):
                if angle < 70 or angle > 100 :
                    back=1
                else:
                    back = 0
            else:
                back = 1
    return back,below

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
        if L_list[i]==0:
            L_list[i]=1
        rad=math.acos((topList[i][0]-botList[i][0])/L_list[i])
        slope=rad*180/math.pi

        if topList[i][1]>=botList[i][1]: #손가락 아래쪽
            slope=slope-180
        else: #손가락 위쪽
            slope = 180 - slope

        S_list.append(slope)
    return S_list

# 손가락 블러 처리하기
def FingerPrintExpress(img,C_list,L_list,S_list,check):
    c_list=[]
    l_list=[]
    s_list=[]
    for i,el in enumerate(check):
        if(check[i]):
            c_list.append([C_list[i][0],C_list[i][1]])
            l_list.append(L_list[i])
            s_list.append(S_list[i])
    for i in range(len(c_list)):
        cx=c_list[i][0]
        cy=c_list[i][1]
        if int(l_list[i]/2)*int(l_list[i]/4)>200:
            cv2.ellipse(img,(int(cx),int(cy)),(int(l_list[i]/2),int(l_list[i]/4)),s_list[i],startAngle=0,endAngle=360,color=(0,0,0),thickness=-1)

def findFingerTipPosition(img,lmList):
    topList=[]
    botList=[]
    for id, lm in enumerate(lmList):
        cx, cy = int(lm[0]), int(lm[1])
        if(id==3 or id==7 or id==11 or id==15 or id==19):
            botList.append([cx,cy])
        elif(id==4 or id==8 or id==12 or id==16 or id==20):
            topList.append([cx,cy])
    return topList,botList

# 거리 구하기
def getDistance(x,y):
    return math.sqrt((x[0]-y[0])*(x[0]-y[0]) + (x[1]-y[1])*(x[1]-y[1]))

# 정확도 측정을 위한 write.csv 파일 생성
f = open('./write.csv','a', newline='')
wr = csv.writer(f)

# # main : input image
for i in os.listdir('./Hands/Hands/'):
    print(i)
    path = './Hands/Hands/' + i 
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    detector = HandDetector(detectionCon=0.7, maxHands=2)
    back1 = 1
    # coloredImg = img.copy()
    height, width, c = img.shape

    # Find the hand and its landmarks
    hands = detector.findHands(img, draw=False)  # with draw
    if hands:
        # 손이 1개 일 경우
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # 21개 랜드마크
        handType1 = hand1["type"]  # Handtype Left or Right

        # 지문 블러처리
        back1, below1 = get_label(handType1,lmList1)
        # if back1 == 0:
        #     topList, botList = findFingerTipPosition(img,lmList1)
        #     L_list=findFingerTipLength(topList,botList)
        #     C_list=findFingerCenter(topList,botList)
        #     S_list=findFingerSlope(topList,botList,L_list)
        #     fingers1 = detector.fingersUp(hand1)
        #     if below1 == 1:
        #         FingerPrintExpress(img,C_list,L_list,S_list,[not i for i in fingers1])
        #     else:
        #         FingerPrintExpress(img,C_list,L_list,S_list,fingers1)
            
        # if len(hands) == 2:
        #     # 손이 2개일 경우
        #     hand2 = hands[1]
        #     lmList2 = hand2["lmList"]  # 21개 랜드마크
        #     handType2 = hand2["type"]  # Hand Type "Left" or "Right"
        #     # 지문 블러처리
        #     back2, below2 = get_label(handType2,lmList2)
        #     if back2 == 0:
        #         topList, botList = findFingerTipPosition(img,lmList2)
        #         L_list=findFingerTipLength(topList,botList)
        #         C_list=findFingerCenter(topList,botList)
        #         S_list=findFingerSlope(topList,botList,L_list)  
        #         fingers2 = detector.fingersUp(hand2)
        #         if below2 == 1:
        #             FingerPrintExpress(img,C_list,L_list,S_list,[not i for i in fingers2])
        #         else:
        #             FingerPrintExpress(img,C_list,L_list,S_list,fingers2)
        # Display
        # cv2.imshow("Image", img)
        
        # 뿌옇게 blur 처9리하기
        # Image_XOR = cv2.bitwise_xor(img, coloredImg)
        # Image_Blur = cv2.medianBlur(Image_XqqOR,3)
        # Prevent_Fingerprints_Image=cv2.add(Image_Blur,img)

        # cv2.imshow("Image", Prevent_Fingerprints_Image)
        # # cv2.imshow("Image", img)
        # out.write(Prevent_Fingerprints_Image)
    if(back1 == 0):
        wr.writerow([i, 1])
    else : 
        wr.writerow([i, 0])
    cv2.imwrite('./output/' + path[14:] , img)
    cv2.destroyAllWindows()
