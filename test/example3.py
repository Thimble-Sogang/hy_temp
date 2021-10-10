import cv2
cam=cv2.VideoCapture(0)
ccfr2=cv2.CascadeClassifier('C:\\palm.xml')
# ccfr2=cv2.CascadeClassifier(cv2.data.haarcascades + '/palm.xml')
while True:
    retval,image=cam.read()
    grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    palm=ccfr2.detectMultiScale(grey,scaleFactor=1.05,minNeighbors=3)
    # for x,y,w,h in palm:
    #     image=cv2.rectangle(image,(x,y),(x+w,y+h),(256,256,256),2)
    print(palm)
    cv2.imshow("Window",image)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        cv2.destroyAllWindows()
        break
del(cam)