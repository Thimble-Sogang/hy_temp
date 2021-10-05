import cv2
import mediapipe as mp
import math

class handDetector():
    def __init__(self,mode=False,maxHands=4,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self,img,draw=False):
        #success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # result에 핸드 info가 들어가는듯?
        # check multiple hand?
        #print(self.results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=False):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 2, (255, 0, 255), cv2.FILLED)

        return lmList

    def findFingerTipPosition(self, img, handNo=0, draw=True):
            lmList = []
            topList=[]
            botList=[]
            if self.results.multi_hand_landmarks:
                for handNo in range(len(self.results.multi_hand_landmarks)):
                    myHand = self.results.multi_hand_landmarks[handNo]

                    for id, lm in enumerate(myHand.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    #lmList.append([id, cx, cy])
                        if(id==3 or id==7 or id==11 or id==15 or id==19):
                            botList.append([cx,cy])
                            if draw:
                                cv2.circle(img, (cx, cy), 3, (0, 0, 0), cv2.FILLED)
                        elif(id==4 or id==8 or id==12 or id==16 or id==20):
                            topList.append([cx,cy])
                            if draw:
                                cv2.circle(img, (cx, cy), 1, (0, 0, 0), cv2.FILLED)

                return topList,botList #lmList
                    # if id==4:
                 # cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

    def findFingerTipLength(self, toplist, botList):
            #return legnth of finger tip point
        L_list=[]
        for i in range(len(toplist)):
                x=toplist[i][0]-botList[i][0]
                y=toplist[i][1]-botList[i][1]
                L_list.append(math.sqrt(x*x + y*y))
        return L_list
    def findFingerCenter(self, toplist,botList):
        #return finger center point list
        C_list=[]
        for i in range(len(toplist)):
            C_list.append([(toplist[i][0]+botList[i][0])/2,(toplist[i][1]+botList[i][1])/2])
        return  C_list
    def findFingerSlope(self,topList,botList,L_list):
        S_list=[]
        for i in range(len(topList)):
            #print(L_list[i])
            #print(botList[i][1]-topList[i][1])
            rad=math.acos((topList[i][0]-botList[i][0])/L_list[i])
            #rad->degree
            slope=rad*180/math.pi

            if topList[i][1]>=botList[i][1]: #손가라 아래쪽
                slope=slope-180
            else: #손가락 위쪽
                #if topList[i][0]>botList[i][0]:
                    slope = 180 - slope

           # print(slope)
            S_list.append(slope)
        return S_list
    def FingerPrintExpress(self,img,C_list,L_list,S_list):
        for i in range(len(C_list)):
            cx=C_list[i][0]
            cy=C_list[i][1]
            cv2.ellipse(img,(int(cx),int(cy)),(int(L_list[i]/2),int(L_list[i]/4)),S_list[i],startAngle=0,endAngle=360,color=(0,0,0),thickness=-1)


