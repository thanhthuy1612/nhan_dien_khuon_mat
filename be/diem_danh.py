import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from matplotlib import pyplot as plt

path = 'Images_Excel'
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
   
def Attendance(name,valmin):
    with open('Diem_danh.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        #if name not in nameList:
        now = datetime.now()
        dtString = now.strftime('%d/%m/%Y, %H:%M:%S')
        f.writelines(f'\n{name},{dtString},{valmin}')
   
encodeListKnown = findEncodings(images)

def diem_danh(src):
    img = cv2.imread(src,cv2.COLOR_BGR2GRAY)
    result = []
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    # so sánh và ghi nhận ID
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis) # get index of min value is true

        # vẽ khung và hiển thị tên
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            valmin = "{}".format(round(100*(1-faceDis[matchIndex])))
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name + ' - ' + valmin +'%',(x1+6,y2-6),cv2.FONT_HERSHEY_PLAIN,4,(0,0,255),2)
            Attendance(name, valmin)
            result.append({"name": name, "percent": valmin})
    now = datetime.now()
    src_new = str(now).replace(" ", "_").replace(":", "-").split(".")[0]
    cv2.imwrite("Diem_Danh/" + src_new + ".jpg", img)
    return result, src_new