import sys
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os

class Thimble (QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Window Setup
        self.resize(1280, 720)
        mainwindow = QMainWindow()
        mainwindow.setGeometry(0, 0, 1280, 720)
        mainwindow.show()
        mainwindow.frameGeometry().moveCenter(QScreen.availableGeometry(QApplication.primaryScreen()).center())
        mainwindow.move(mainwindow.frameGeometry().topLeft())

        # Open file
        #fileName, _ = QFileDialog.getOpenFileName(self, "파일 열기", "", "All Files (*)")


        self.grid = QGridLayout()

        self.setLayout(self.grid)


        self.image_frame1 = QLabel()
        self.image_frame1.setStyleSheet("border-style: solid;"
                                        "border-width: 2px;"
                                        "border-color: #000000;")
        self.grid.addWidget(self.image_frame1, 1, 1)

        self.image_frame2 = QLabel()
        self.image_frame2.setStyleSheet("border-style: solid;"
                                        "border-width: 2px;"
                                        "border-color: #000000;")
        self.grid.addWidget(self.image_frame2, 1, 2)


        self.label1 = QLabel('', self)
        self.label1.setStyleSheet("border-style: solid;"
                                "border-width: 1px;"
                                "border-color: #000000;"
                                "border-radius: 3px")

        self.label2 = QLabel('', self)
        self.label2.setStyleSheet("border-style: solid;"
                                "border-width: 1px;"
                                "border-color: #000000;"
                                "border-radius: 3px")


        addbutton1 = QPushButton('Open File', self)

        self.grid.addWidget(self.label1, 2, 1)

        self.grid.addWidget(addbutton1, 2, 2)


        addbutton1.clicked.connect(self.add_open)

        addbutton2 = QPushButton('Save File', self)

        self.grid.addWidget(self.label2, 3, 1)

        self.grid.addWidget(addbutton2, 3, 2)

        addbutton2.clicked.connect(self.add_save)

    def add_open(self):
        self.fileName = QFileDialog.getOpenFileName(self, 'Open file', './')

        self.label1.setText(self.fileName[0])
        
    def add_save(self):

        self.saveName = QFileDialog.getSaveFileName(self, 'Save file', './')

        self.label2.setText(self.saveName[0])

        addbutton3 = QPushButton('run Timble', self)
        
        self.grid.addWidget(addbutton3, 4, 2)

        extension = self.fileName[0].split('.')[len(self.fileName[0].split('.'))-1].lower()

        if extension == "jpg" or extension == "jpeg" or extension == "bmp" or extension == "png" or extension == "jpg" :
            addbutton3.clicked.connect(self.run_ThimbleImage)
        else :
            addbutton3.clicked.connect(self.run_ThimbleVideo)
        # change Video        

    def run_ThimbleVideo(self):
        print(self.fileName[0])
        print(self.saveName[0])
        cap = cv2.VideoCapture(self.fileName[0])
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter(self.saveName[0], fourcc, fps, (int(width), int(height)))

        detector = HandDetector(detectionCon=0.7, maxHands=2)
        while True:
            # Get image frame
            success, img = cap.read()
            # coloredImg = img.copy() for realBlur
            if success == False :
                break
            unModifiedImg = img.copy()
            # Find the hand and its landmarks
            hands = detector.findHands(img, draw=False)  # with draw

            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            self.send_image = QImage(rgbImage, int(width), int(height), img.shape[1] * 3, QImage.Format_RGB888)
            self.send_image = self.send_image.scaledToWidth(640)
            self.image_frame1.setPixmap(QPixmap.fromImage(self.send_image))

            if hands:
               # 손이 1개 일 경우
                hand1 = hands[0]
                lmList1 = hand1["lmList"]  # 21개 랜드마크
                handType1 = hand1["type"]  # Handtype Left or Right

                # 지문 블러처리
                back1, below1 = self.get_label(handType1,lmList1)
                if back1 == 0:
                    topList, botList = self.findFingerTipPosition(img,lmList1)
                    L_list = self.findFingerTipLength(topList,botList)
                    C_list = self.findFingerCenter(topList,botList)
                    S_list = self.findFingerSlope(topList,botList,L_list)
                    fingers1 = detector.fingersUp(hand1)
                    if below1 == 1:
                        self.FingerPrintExpress(img,C_list,L_list,S_list,[not i for i in fingers1])
                    else:
                        self.FingerPrintExpress(img,C_list,L_list,S_list,fingers1)

                if len(hands) == 2:
                    # 손이 2개일 경우
                    hand2 = hands[1]
                    lmList2 = hand2["lmList"]  # 21개 랜드마크
                    handType2 = hand2["type"]  # Hand Type "Left" or "Right"
                    # 지문 블러처리
                    back2, below2 = self.get_label(handType2,lmList2)
                    if back2 == 0:
                        topList, botList = self.findFingerTipPosition(img,lmList2)
                        L_list = self.findFingerTipLength(topList,botList)
                        C_list = self.findFingerCenter(topList,botList)
                        S_list = self.findFingerSlope(topList,botList,L_list)  
                        fingers2 = detector.fingersUp(hand2)
                        if below2 == 1:
                            self.FingerPrintExpress(img,C_list,L_list,S_list,[not i for i in fingers2])
                        else:
                            self.FingerPrintExpress(img,C_list,L_list,S_list,fingers2)

            # 검은 블러 처리
            out.write(img)
            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            self.send_image = QImage(rgbImage, int(width), int(height), img.shape[1] * 3, QImage.Format_RGB888)
            self.send_image = self.send_image.scaledToWidth(640)
            self.image_frame2.setPixmap(QPixmap.fromImage(self.send_image))

            # 뿌옇게 blur 처리하기
            # Image_XOR = cv2.bitwise_xor(img,unModifiedImg)
            # Image_Blur = cv2.bilateralFilter(Image_XOR,9,75,75)
            # Prevent_Fingerprints_Image=cv2.add(Image_Blur,img)

            # rgbImage = cv2.cvtColor(Prevent_Fingerprints_Image, cv2.COLOR_BGR2RGB)
            # self.send_image = QImage(rgbImage, int(width), int(height), img.shape[1] * 3, QImage.Format_RGB888)
            # self.send_image = self.send_image.scaledToWidth(640)
            # self.image_frame2.setPixmap(QPixmap.fromImage(self.send_image))
            # out.write(Prevent_Fingerprints_Image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()


    def run_ThimbleImage(self):
        ff = np.fromfile(self.fileName[0], np.uint8)
        img = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
        detector = HandDetector(detectionCon=0.7, maxHands=2)
        unModifiedImg = img.copy()
        
        width= np.shape(img)[0]
        height= np.shape(img)[1]
        hands = detector.findHands(img, draw=False)  # with draw

        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.send_image = QImage(rgbImage, int(width), int(height), width * 3, QImage.Format_RGB888)
        self.send_image = self.send_image.scaledToWidth(640)
        self.image_frame1.setPixmap(QPixmap.fromImage(self.send_image))

        if hands:
            # 손이 1개 일 경우
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # 21개 랜드마크
            handType1 = hand1["type"]  # Handtype Left or Right

            # 지문 블러처리
            back1, below1 = self.get_label(handType1,lmList1)
            if back1 == 0:
                topList, botList = self.findFingerTipPosition(img,lmList1)
                L_list = self.findFingerTipLength(topList,botList)
                C_list = self.findFingerCenter(topList,botList)
                S_list = self.findFingerSlope(topList,botList,L_list)
                fingers1 = detector.fingersUp(hand1)
                if below1 == 1:
                    self.FingerPrintExpress(img,C_list,L_list,S_list,[not i for i in fingers1])
                else:
                    self.FingerPrintExpress(img,C_list,L_list,S_list,fingers1)

            if len(hands) == 2:
                # 손이 2개일 경우
                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # 21개 랜드마크
                handType2 = hand2["type"]  # Hand Type "Left" or "Right"
                # 지문 블러처리
                back2, below2 = self.get_label(handType2,lmList2)
                if back2 == 0:
                    topList, botList = self.findFingerTipPosition(img,lmList2)
                    L_list = self.findFingerTipLength(topList,botList)
                    C_list = self.findFingerCenter(topList,botList)
                    S_list = self.findFingerSlope(topList,botList,L_list)  
                    fingers2 = detector.fingersUp(hand2)
                    if below2 == 1:
                        self.FingerPrintExpress(img,C_list,L_list,S_list,[not i for i in fingers2])
                    else:
                        self.FingerPrintExpress(img,C_list,L_list,S_list,fingers2)

            # 검은 블러 처리
            self.imwrite(self.saveName[0], img)
           
            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            self.send_image = QImage(rgbImage, int(width), int(height), width * 3, QImage.Format_RGB888)
            self.send_image = self.send_image.scaledToWidth(640)
            self.image_frame2.setPixmap(QPixmap.fromImage(self.send_image))

            #뿌옇게 blur 처리하기
            # Image_XOR = cv2.bitwise_xor(img,unModifiedImg)
            # Image_Blur = cv2.bilateralFilter(Image_XOR,9,75,75)
            # Prevent_Fingerprints_Image=cv2.add(Image_Blur,img)

            # rgbImage = cv2.cvtColor(Prevent_Fingerprints_Image, cv2.COLOR_BGR2RGB)
            # self.send_image = QImage(rgbImage, int(width), int(height), img.shape[1] * 3, QImage.Format_RGB888)
            # self.send_image = self.send_image.scaledToWidth(640)
            # self.image_frame2.setPixmap(QPixmap.fromImage(self.send_image))
            # self.imwrite(self.saveName[0], Prevent_Fingerprints_Image)
            
            
    # 내부 함수
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def imwrite(self, filename, img, params=None):
        try: 
            ext = os.path.splitext(filename)[1] 
            result, n = cv2.imencode(ext, img, params) 

            if result: 
                with open(filename, mode='w+b') as f: 
                    n.tofile(f)
                return True
            else:
                return False
        except Exception as e: 
            print(e) 
            return False

    def getAngle(self, lmList):
        x1 = lmList[1][0] - lmList[0][0]
        y1 = lmList[1][1] - lmList[0][1]
        x2 = lmList[17][0] - lmList[0][0]
        y2 = lmList[17][1] - lmList[0][1]
        rad = math.acos((x1*x2 + y1*y2) / (self.getDistance(lmList[1],lmList[0]) * self.getDistance(lmList[17],lmList[0])))
        slope=rad*180/math.pi
        return slope

    def get_label(self, type,lmList):
        back = 1
        below = 0
        angle = self.getAngle(lmList)
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

    def findFingerSlope(self, topList,botList,L_list):
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
    def FingerPrintExpress(self, img,C_list,L_list,S_list,check):
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

    def findFingerTipPosition(self, img,lmList):
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
    def getDistance(self, x,y):
        return math.sqrt((x[0]-y[0])*(x[0]-y[0]) + (x[1]-y[1])*(x[1]-y[1]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Thimble()
    win.setWindowTitle('Thimble')
    win.setWindowIcon(QIcon("src/image/logo.jpg"))
    win.show()

    sys.exit(app.exec_())