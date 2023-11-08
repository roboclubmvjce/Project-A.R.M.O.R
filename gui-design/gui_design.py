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

#Menu
menubar = tkb.Menu(window)
window.config(menu=menubar)
file_menu = tkb.Menu(menubar,tearoff=0)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

camera_menu=tkb.Menu(menubar,tearoff=0)
camera_menu.add_command(label="RGB")
camera_menu.add_command(label="Depth")

option_menu=tkb.Menu(menubar,tearoff=0)
option_menu.add_command(label="Exit")

edit_menu = tkb.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")


menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Camera",menu=camera_menu)
menubar.add_cascade(label="Option",menu=option_menu)
menubar.add_cascade(label="Edit", menu=edit_menu)


#Tabs
notebook = tkb.Notebook(window)
notebook.pack(expand=True,fill = tkb.BOTH)
tab1 = tkb.Frame(notebook)
tab2 = tkb.Frame(notebook)
tab3 = tkb.Frame(notebook)

notebook.add(tab1, text='Img. Proc.')
notebook.add(tab2, text='Sensor Data')
notebook.add(tab3, text='Extras')

face = tkb.Button(tab1,text='Face',width=10)
face.place(x=5,y=2)
person = tkb.Button(tab1,text='Person',width=10)
person.place(x=5,y=35)
boxes = tkb.Button(tab1,text='Boxes',width=10)
boxes.place(x=5,y=68)
chair = tkb.Button(tab1,text='Chair',width=10,)
chair.place(x=5,y=101)



update_camera()
window.mainloop()
