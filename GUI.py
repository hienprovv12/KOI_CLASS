from random import sample
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter 
from threading import Thread
import cv2
import PIL.Image,PIL.ImageTk
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import model_from_json,load_model
from tensorflow.keras.optimizers import SGD
from keras.preprocessing.image import load_img,img_to_array
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfilename


list_name = ["Asagi","Bekko_Hi","Bekko_Ki","Bekko_Shiro","Ghosiki","Goromo","Kohaku","Kujaku","Ogon_Orenji","Ogon_Platinum","Ogon_Yamabuki","Showa_Sanshoku","Shusui","Taisho_Sanke","Tancho","Utsuri_Hi","Utsuri_Ki","Utsuri_Shiro"]

model_weights = "model_v3.h5"
model=load_model(model_weights)
isOn = 0



def compare():
    global sample
    global frame
    global pos
    global canvas, photo
    global ret
    roi = frame
    if ret == False:
        return
    img = cv2.resize(roi,(250,250))
    img = img.reshape(1,250,250,3)
    img = img.astype('float32')
    img = img/255.0
    pos = int(np.argmax(model.predict(img)))
    patio = np.max(model.predict(img))*100
    patio = round(patio,4)
    print(list_name[pos])
    
def onOpenVideo():
    global file
    global video
    global canvas,photo
    global ret,frame, pos
    global isOn
    file = askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv"),("All files", "*.*") ))
    video = cv2.VideoCapture(file)
    canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    canvas.config(width=canvas_w,height=canvas_h)
    print(file)
    ret,frame = video.read()
    frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
    canvas.create_image(0,0,image=photo,anchor=tkinter.NW) 
    video = cv2.VideoCapture(file)    

def onOpenCamera():
    global file
    global video
    global canvas,photo
    global ret,frame, pos
    global isOn
    video = cv2.VideoCapture(0)    
    canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    canvas.config(width=canvas_w,height=canvas_h)
    
def onVideo():
    global isOn
    isOn=1
    print(isOn)
    
def onCamera():
    global isOn
    isOn=2

def onStop():
    global isOn
    isOn=0
window = Tk()
window.title('Koi application')
window.geometry("1024x668")



label1 = Label(text='',font=("Arial", 15))
label1.place(x=10,y=10)
btnOn = Button(window,text="OPEN VIDEO",command=onOpenVideo)
btnOn.place(x=200,y=10)
btnOn = Button(window,text="RUN VIDEO",command=onVideo)
btnOn.place(x=300,y=10)
btnOn = Button(window,text="STOP",command=onStop)
btnOn.place(x=400,y=10)

btnOn = Button(window,text="OPEN CAMERA",command=onOpenCamera)
btnOn.place(x=500,y=10)
btnOn = Button(window,text="RUN CAMERA",command=onCamera)
btnOn.place(x=600,y=10)

pos=0
canvas = Canvas(window,width=100,height=100,bg='blue')
canvas.place(x=10,y=40)


def update_frame():
    global canvas,photo
    global ret,frame, pos
    global isOn
    global image,video

    if isOn == 1:
        ret,frame = video.read()
        if ret == False:
            isOn=0
            window.after(200,update_frame)
            return
        frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        thread = Thread(target=compare)
        thread.start()
        label1.config(text=list_name[pos],font=("Arial", 15))
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
        canvas.create_image(0,0,image=photo,anchor=tkinter.NW)
        
    if isOn == 2:
        ret,frame = video.read()
        if ret == False:
            isOn=0
            window.after(200,update_frame)
            return
        frame1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame1 = cv2.flip(frame1, 1)
        thread = Thread(target=compare)
        thread.start()
        label1.config(text=list_name[pos],font=("Arial", 15))
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
        canvas.create_image(0,0,image=photo,anchor=tkinter.NW)
    
    window.after(200,update_frame)

update_frame()
window.mainloop()



