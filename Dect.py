#coding=utf8 
from Tkinter import *
import tkMessageBox
import cv2  
import cv2.cv as cv  
import requests  
import json
import os

capture = cv.CaptureFromCAM(0)
root = None;
name_input = None;
filename = "/home/pi/Desktop/face.jpg";
dect_filename = "/home/pi/Desktop/face_dect.jpg"
api_key = "sAnx5RjAiDfEV5c2Bsd8ukDL18MkTIBZ"
api_secret = "738-qd7pLyFOp4ngHVXu0Ic3QZUbhrdt"
add_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'  
add_set_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'  
compare_url = 'https://api-cn.faceplusplus.com/facepp/v3/search'

def open_dect_cam():   
    while True:    
        img = cv.QueryFrame(capture)  
        cv.ShowImage("人脸识别",img)    
        key = cv.WaitKey(10)    
        if key == 1048603:    
            break    
        if key == 1048608:
            if(os.path.exists(dect_filename)):
                os.remove(dect_filename)
            cv.SaveImage(dect_filename,img)
            print "图片截取成功"
            search()
            break;  

def search():
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
        face_token = str(data["results"][0]["face_token"])
        confidence = float(data["results"][0]["confidence"])
        user_id = str(data["results"][0]["user_id"])
        msg = user_id+'可靠度为：'+str(confidence)
        if(confidence>=85):
            tkMessageBox.showinfo(title='您是：', message=msg)
        else:
            tkMessageBox.showinfo(title='非法用户：', message='非法用户')

while True:
    open_dect_cam()
    cv2.destroyAllWindows() 

