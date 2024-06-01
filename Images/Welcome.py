import os
import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image , ImageTk 
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time
import sqlite3

global fn
fn=""
root = tk.Tk()
root.configure(background="seashell2")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("MAIN PAGE")


frame_alpr = tk.LabelFrame(root, width=1850, height=1850, bd=5, font=('times', 14, ' bold '),bg="#013220")
frame_alpr.grid(row=0, column=0)
frame_alpr.place(x=0, y=0)

image2 =Image.open('Images/welcome_front.jpg')
image2 =image2.resize((140,120))

background_image=ImageTk.PhotoImage(image2)
background_label = tk.Label(frame_alpr, image=background_image)

background_label.image = background_image

background_label.place(x=680, y=25)

lbl = tk.Label(frame_alpr, text="PLANT DISEASE DETECTION ", font=('Times New Roman', 35,' bold '),bg="#013220",fg="white")
lbl.place(x=425, y=180)

lbl = tk.Label(frame_alpr, text="AND CURE RECCOMENDATION", font=('Times New Roman', 35,' bold '),bg="#013220",fg="white")
lbl.place(x=400, y=250)

logo_label=tk.Label()
logo_label.place(x=300,y=55)


logo_label1=tk.Label(text='System that capable \n to Detect And \n Identify the type of disease...',compound='bottom',font=("Times New Roman", 20, 'bold', 'italic'),width=35, bg="#cce6ff", fg="black")
logo_label1.place(x=500,y=590)

   
def window():
    root.destroy()
def open_login_page():
    os.system('python Login.py')
button1 = tk.Button(frame_alpr, text=" START",command=open_login_page,width=15, height=1, font=('times', 15, ' bold '),bg="#3BB9FF",fg="black")
button1.place(x=650, y=450)

root.mainloop()