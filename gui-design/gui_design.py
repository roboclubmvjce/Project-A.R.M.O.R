import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tkb
import cv2
from PIL import Image,ImageTk

#tkinter window stats
window = tk.Tk()
window.title('A.R.M.O.R') #window name
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry('%dx%d'%(width,height)) #dimensions of window
style = tkb.Style('darkly') #window theme
window.bind('<Escape>', lambda e: window.quit())

x_position = (width - 1400) // 2
label =tkb.Label(window)
label.pack(padx=x_position,pady=0)
cap= cv2.VideoCapture(0)

def update_camera():
    global cap
    _, frame = cap.read()
    if _:
        # Resize the frame to the desired width and height
        desired_width = 1400
        desired_height = 450
        frame = cv2.resize(frame, (desired_width, desired_height))

        # Convert the frame to RGB format for tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create a tkinter-compatible photo image
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo

        # Call the function recursively after 10 milliseconds to update the camera feed
        label.after(10, update_camera)

update_camera()
window.mainloop()
