from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tkb
import cv2
from PIL import Image,ImageTk

#tkinter window stats
window = Tk()
window.title('A.R.M.O.R') #window name
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry('%dx%d'%(width,height)) #dimensions of window
style = tkb.Style('darkly') #window theme
window.bind('<Escape>', lambda e: window.quit())
x_position = (width - 1400) // 2
label =tkb.Label(window)
label.pack(padx=x_position,pady=0)

#CV variables
cap= cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
green = (0,255,0)

def update_camera():
    global cap
    _, frame = cap.read()
    if _:
        # Resize the frame to the desired width and height
        desired_width = 640
        desired_height = 480
        frame = cv2.resize(frame, (desired_width, desired_height))    
        face_proc(frame)
        # Convert the frame to RGB format for tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create a tkinter-compatible photo image
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo

        # Call the function recursively after 10 milliseconds to update the camera feed
        label.after(10, update_camera)

# Facial Recognition
def face_proc(frame):
    face = face_cascade.detectMultiScale(frame,
        scaleFactor = 2,
        minNeighbors = 5)
    if face_var.get() == 1:
        for x,y,w,h in face:
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),green,3) # This draws boxes around detected faces
                cv2.putText(frame,str("Face"), (x,y-5),cv2.FONT_HERSHEY_PLAIN, 2,green,2)

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
notebook = tkb.Notebook(window,bootstyle ='danger')
notebook.pack(expand=True,fill = tkb.BOTH)
tab1 = tkb.Frame(notebook)
tab2 = tkb.Frame(notebook)
tab3 = tkb.Frame(notebook)

notebook.add(tab1, text='Img. Proc.')
notebook.add(tab2, text='Sensor Data')
notebook.add(tab3, text='Extras')

tab1_frame = tkb.Frame(tab1, bootstyle='darkly' ,border=5,borderwidth=5)
tab1_frame.place(x=20,y=10,width = 200,height=200)

#img processing variables
face_var = IntVar()
person_var = IntVar()
boxes_var = IntVar()
chair_var = IntVar()
vehicle_var = IntVar()
All_var = IntVar()

face = tkb.Label(tab1_frame,text='Face',font=('Helvetica', 18),bootstyle='danger, inverse',width=12)
face.place(x=10,y=2)
face_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=face_var,)
face_check.place(x=120,y=10)
person = tkb.Label(tab1_frame,text='Person',font=('Helvetica', 18),bootstyle='danger, inverse',width=12)
person.place(x=10,y=35)
person_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=person_var)
person_check.place(x=120,y=43)
boxes = tkb.Label(tab1_frame,text='Boxes',font=('Helvetica', 18),bootstyle='danger, inverse',width=12)
boxes.place(x=10,y=68)
boxes_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=boxes_var)
boxes_check.place(x=120,y=76)
chair = tkb.Label(tab1_frame,text='Chair',font=('Helvetica', 18),bootstyle='danger, inverse',width=12)
chair.place(x=10,y=101)
chair_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=chair_var)
chair_check.place(x=120,y=109)
vehicle = tkb.Label(tab1_frame,text='Vehicle',font=('Helvetica', 18),bootstyle='danger, inverse',width=12)
vehicle.place(x=10,y=134)
vehicle_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=vehicle_var)
vehicle_check.place(x=120,y=142)
EnableAll = tkb.Label(tab1_frame,text='Enable All',font=('Helvetica', 16),bootstyle='danger, inverse',width=13)
EnableAll.place(x=10,y=167)
EnableAll_check = tkb.Checkbutton(tab1_frame,bootstyle ='success',onvalue=1,offvalue=0,variable=All_var)
EnableAll_check.place(x=125,y=175)


update_camera()
window.mainloop()