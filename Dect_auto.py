#coding=utf8 
from Tkinter import *
import tkMessageBox
import cv2  
import cv2.cv as cv  
import requests  
import json
import os
import time
#capture = cv.CaptureFromCAM(0)
root = None;
name_input = None;
filename = "/home/pi/Desktop/face.jpg";
dect_filename = "/home/pi/Desktop/face_dect.jpg"
api_key = "sAnx5RjAiDfEV5c2Bsd8ukDL18MkTIBZ"
api_secret = "738-qd7pLyFOp4ngHVXu0Ic3QZUbhrdt"
add_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'  
add_set_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'  
compare_url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
faceCascade = cv2.CascadeClassifier("/home/pi/Desktop/haarcascade_frontalface_default.xml") #1

def open_dect_cam():
    lasttime = 0
    currenttime =0
    cascade = cv2.CascadeClassifier("/home/pi/Desktop/haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    first = True
    while True:
        currenttime=time.time()
        #img = cv.QueryFrame(capture)
        ret,frame = cap.read()
        cv2.waitKey(10) 
        #print(currenttime - lasttime )
        if currenttime - lasttime >= 5 and first==False:
            #r = random.randint(0,90)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            rect = cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=1,minSize=(50,50),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
            for x,y,z,w in rect:
                cv2.rectangle(frame,(x,y),(x+z,y+w),(0,0,255),2)
            lasttime = currenttime
            if len(rect)!=0 :
                print("face rect")
                if(os.path.exists(dect_filename)):
                    os.remove(dect_filename)
                cv2.imwrite(dect_filename,frame)
                print "图片截取成功"
                search()
                break;
        
        if first :
            lasttime = currenttime;
            first = False
        
        cv2.imshow('frame',frame)

def search():
    img = cv2.imread(dect_filename)  
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    rect = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=1,minSize=(50,50),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    if(len(rect) != 0):
        print(len(rect))
        payload = {'api_key': api_key,  
               'api_secret': api_secret,  
               'outer_id':'inet',  
               }  
        files = {'image_file':open(dect_filename, 'rb')}  
        r = requests.post(compare_url,files=files,data=payload)  
        data=json.loads(r.text)
        print(r.text)
        if(r.status_code != 200):
            print("request exception")
        else:
            if data["results"] != None:
                face_token = str(data["results"][0]["face_token"])
                confidence = float(data["results"][0]["confidence"])
                user_id = str(data["results"][0]["user_id"])
                msg = user_id+'可靠度为：'+str(confidence)
                if(confidence>=85):
                    print('您是：'+msg)
                    #tkMessageBox.showinfo(title='您是：', message=msg)
                else:
                    print('您是：'+'非法用户')
                    #tkMessageBox.showinfo(title='非法用户：', message='非法用户')
            else:
                tkMessageBox.showinfo(title='识别错误：', message='请重试！')
    else:
        tkMessageBox.showinfo(title='识别错误：', message='未识别到人脸！')

while True:
    try:
        open_dect_cam()
        cv2.destroyAllWindows() 
    except Exception as msg:
        print(msg)
        continue;
