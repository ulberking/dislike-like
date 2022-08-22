import cv2
import mediapipe as mp

camera = cv2.VideoCapture(0)
mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)
fingertip=[8,12,16,20]
thumbtip=4
def drawLandmarks(image,handlandmarks):
    if(handlandmarks):
        for i in handlandmarks:
            mp_drawing.draw_landmarks(image,i,mp_hands.HAND_CONNECTIONS)
def  count_fingers(image,handlandmarks,handnumber=0):
    if(handlandmarks):
        for hl in handlandmarks:
            lmlist=[]
            for lm in hl.landmark:
                lmlist.append(lm)
        fingerstatus=[]
        for i in fingertip:
            x,y=int(lmlist[i].x*width),int(lmlist[i].y*height)
            cv2.circle(image,(x,y),3,(255,0,0),cv2.FILLED)
            if(lmlist[i].x<lmlist[i-2].x):
                fingerstatus.append(1)
            else:
                fingerstatus.append(0)
        total_finger=fingerstatus.count(1)
        if(total_finger==4):
            if(lmlist[thumbtip].y<lmlist[thumbtip-1].y<lmlist[thumbtip-2].y):
                cv2.putText(image ,"LIKE", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            elif(lmlist[thumbtip].y>lmlist[thumbtip-1].y>lmlist[thumbtip-2].y):
                 cv2.putText(image ,"DISLIKE", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

while True:
    ret,image=camera.read()
    image=cv2.flip(image,1)
    height,width,channels=image.shape
    results=hands.process(image)
    handlandmarks=results.multi_hand_landmarks
    drawLandmarks(image,handlandmarks)
    count_fingers(image,handlandmarks)
    cv2.putText(image ,"Use your left hand only", (200,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
    cv2.imshow('result',image)
    if(cv2.waitKey(1)==32):
        break
camera.release()
cv2.destroyAllWindows()