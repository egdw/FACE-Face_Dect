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

def on_click():
    username = name_input.get()
    print(username)
    root.destroy()
    addUser(username)
    
def open_cam():   
    while True:    
        img = cv.QueryFrame(capture)  
        cv.ShowImage("人脸录入",img)    
        key = cv.WaitKey(10)    
        if key == 1048603:    
            break    
        if key == 1048608:
            if(os.path.exists(filename)):
                os.remove(filename)
            cv.SaveImage(filename,img) 
            print "图片截取成功"
            break;

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
            break;
        
def addUser(username):
    files = {'image_file':open(filename, 'rb')}  
    payload = {'api_key': 'sAnx5RjAiDfEV5c2Bsd8ukDL18MkTIBZ',  
               'api_secret': '738-qd7pLyFOp4ngHVXu0Ic3QZUbhrdt',  
               'return_landmark': 0,  
               'return_attributes':'gender,age,glass'}  
       
    r = requests.post(add_url,files=files,data=payload)  
    data=json.loads(r.text)  
    print(r.text)  
    width = data['faces'][0]['face_rectangle']['width']  
    top = data['faces'][0]['face_rectangle']['top']  
    height = data['faces'][0]['face_rectangle']['height']  
    left = data['faces'][0]['face_rectangle']['left']  
    face_token = str(data['faces'][0]['face_token'])
    gender = str(data['faces'][0]['attributes']['gender']['value'])
    age = str(data['faces'][0]['attributes']['age']['value'])
    glass = str(data['faces'][0]['attributes']['glass']['value'])
    print(face_token)
    print(age)
    print(glass)
    img = cv2.imread(filename)  
    vis = img.copy()  
    cv2.rectangle(vis, (left, top), (left+width, top+height),(0, 255, 0), 2)  
    cv2.imshow("识别结果", vis)
    msg = 'gender:'+gender+'age:'+age+'wear glass:'+glass
    tkMessageBox.showinfo(title='识别到的信息：', message=msg)
    cv2.waitKey (0)
    cv2.destroyAllWindows()
    add_to_set(face_token,username)
    
def add_to_set(face_token,username):
    payload = {'api_key': api_key,  
           'api_secret': api_secret,   
           'outer_id':'inet',  
           'face_tokens':face_token  
           }  
    r = requests.post(add_set_url,data=payload)
    print('tianjiajihe'+r.text)
    setUserId(face_token,username)
    open_dect_cam()
    search()
    

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
        if(confidence>=85):
            tkMessageBox.showinfo(title='您是：', message=user_id)
        else:
            tkMessageBox.showinfo(title='非法用户：', message='非法用户')
    

def getUserDetail(face_token):
    payload = {'api_key': api_key,  
               'api_secret': api_secret,  
               'face_token':face_token,
               }
    r = requests.post('https://api-cn.faceplusplus.com/facepp/v3/face/getdetail',data=payload)
    print('chaxungengduo'+r.text)
    data=json.loads(r.text)
    user_id = data['user_id']
    tkMessageBox.showinfo(title='您是：', message=user_id)
    

def setUserId(face_token,username):
    payload = {'api_key': api_key,  
               'api_secret': api_secret,  
               'face_token':face_token,
               'user_id':username,
               }
    print(api_key)
    print(face_token)
    print(username)
    r = requests.post('https://api-cn.faceplusplus.com/facepp/v3/face/setuserid',data=payload)
    print('shezhi id'+r.text)
    
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 100
root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10, (screen_width - root.winfo_width())/2, (screen_height - root.winfo_height())/2) ) 
root.title("请输入您的姓名(千万不要写错)")
root.geometry('300x50')
name_input = StringVar()
name = Entry(root,textvariable=name_input)
Button(root, text="确定", command = on_click).pack()
name.pack()
open_cam()
cv2.destroyAllWindows()
name_input.set("")
root.mainloop()