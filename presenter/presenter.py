#!/usr/bin/env python3

import rtmidi
import time
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from threading import Thread
from CK_Setup import Setup, BColors

image1 = "images/codeKlavier.jpg"

im1 = Image.open(image1)

draw = ImageDraw.Draw(im1)
#draw1 = ImageDraw.Draw(im1)
#draw1.line((0, im1.size[1], im1.size[0], 0), 128, 3)
#del draw1

root = tk.Tk()
tkim = ImageTk.PhotoImage(im1)

label = tk.Label(root, fg="blue")
label.pack()

counter = 0 
def counter_label(label):
    def count():
        global counter
        counter += 1
        label.config(text=str(counter))
        label.after(1000, count)
    count()
    
def test(label):
    def run():
        global pointx, pointy
        pointxn = pointx + 1
        pointyn = pointy + 1
        draw.line((pointx, pointy, pointxn, pointyn), 125, 3)

        label.config(image=tkim)
        label.image=tkim
        label.after(100, run)
    run()

pointx = 2 
pointy = 1
#test(10,label)
#counter_label(label)
dt = Thread(target=test(label))    
dt.start()
root.mainloop()

#print(im1.format, im1.size, im1.mode)

#out = im1.rotate(45)

#out.show()
