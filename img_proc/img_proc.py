from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tkb
import cv2
from PIL import Image,ImageTk
import time , os 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.animation as animation
import matplotlib as plt


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

def file_loc(filename):
    for root, _, files in os.walk('.'):
        if filename in files:
            return os.path.join(root, filename)

#CV variables
cap= cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
yolo_weights = file_loc("yolov4-tiny.weights")
yolo_tiny_cfg = file_loc("yolov4-tiny.cfg")
classes_txt = file_loc("classes.txt")
net=cv2.dnn.readNet(yolo_weights,yolo_tiny_cfg)
model=cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320),scale=1/255)
classes=[]
prevFrameTime = 0
currentFrameTime = 0
green = (0,255,0)

with open(classes_txt,"r") as file_object:
    for class_name in file_object.readlines():
        class_name=class_name.strip()
        classes.append(class_name)



def update_camera():
    global cap
    global prevFrameTime, currentFrameTime
    currentFrameTime = time.time()
    fps = 1 / (currentFrameTime - prevFrameTime)
    prevFrameTime = currentFrameTime
    
    _, frame = cap.read()
    if _:
        # Resize the frame to the desired width and height
        desired_width = 640
        desired_height = 480
        frame = cv2.resize(frame, (desired_width, desired_height))    
        face_proc(frame)
        person_proc(frame)
        all_proc(frame)
        #To get FPS
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # Convert the frame to RGB format for tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Create a tkinter-compatible photo image
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
        # Call the function recursively after 10 milliseconds to update the camera feed
        label.after(5, update_camera)

# Facial Recognition
def face_proc(frame):
    face = face_cascade.detectMultiScale(frame,
        scaleFactor = 2,
        minNeighbors = 5)
    if face_var.get() == 1:
        for x,y,w,h in face:
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),green,3) # This draws boxes around detected faces
                cv2.putText(frame,str("Face"), (x,y-5),cv2.FONT_HERSHEY_PLAIN, 2,green,2)

def person_proc(frame):
    if person_var.get()==1:
        (class_ids, scores, bboxes) = model.detect(frame)
        for class_id,scores,bbox in zip(class_ids,scores,bboxes):
            (x,y,w,h)=bbox
            class_name=classes[class_id]
            if class_name =='person':
                cv2.putText(frame,class_name, (x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

def all_proc(frame):
    if all_var.get()==1:
        (class_ids, scores, bboxes) = model.detect(frame)
        for class_id,scores,bbox in zip(class_ids,scores,bboxes):
            (x,y,w,h)=bbox
            class_name=classes[class_id]
            cv2.putText(frame,class_name, (x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

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
notebook = tkb.Notebook(window,bootstyle ='primary')
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
all_var = IntVar()

face = tkb.Label(tab1_frame,text='Face',font=('Helvetica', 18),bootstyle='primary, inverse',width=12)
face.place(x=10,y=2)
face_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=face_var,)
face_check.place(x=120,y=10)
person = tkb.Label(tab1_frame,text='Person',font=('Helvetica', 18),bootstyle='primary, inverse',width=12)
person.place(x=10,y=35)
person_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=person_var)
person_check.place(x=120,y=43)
boxes = tkb.Label(tab1_frame,text='Boxes',font=('Helvetica', 18),bootstyle='primary, inverse',width=12)
boxes.place(x=10,y=68)
boxes_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=boxes_var)
boxes_check.place(x=120,y=76)
chair = tkb.Label(tab1_frame,text='Chair',font=('Helvetica', 18),bootstyle='primary, inverse',width=12)
chair.place(x=10,y=101)
chair_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=chair_var)
chair_check.place(x=120,y=109)
vehicle = tkb.Label(tab1_frame,text='Vehicle',font=('Helvetica', 18),bootstyle='primary, inverse',width=12)
vehicle.place(x=10,y=134)
vehicle_check = tkb.Checkbutton(tab1_frame,bootstyle ='info ,round-toggle',onvalue=1,offvalue=0,variable=vehicle_var)
vehicle_check.place(x=120,y=142)
EnableAll = tkb.Label(tab1_frame,text='Enable All',font=('Helvetica', 16),bootstyle='primary, inverse',width=13)
EnableAll.place(x=10,y=167)
EnableAll_check = tkb.Checkbutton(tab1_frame,bootstyle ='success',onvalue=1,offvalue=0,variable=all_var)
EnableAll_check.place(x=125,y=175)

#sensor data tab
def generate_data():#Create a function to generate random data for the graphs
    return [random.randint(0, 100) for _ in range(10)]

def update_graphs(i):# Create a function to update the graphs with new data
    data1 = generate_data()
    ax1.clear()
    ax1.plot(data1, label='Graph 1')
    ax1.set_title('CPU TEMP')

# Create Figure and Axes for the graphs
fig = Figure(figsize=(4, 2), dpi=100)
ax1 = fig.add_subplot(111)

# Create FigureCanvasTkAgg widgets to display the graphs in the tab
canvas = FigureCanvasTkAgg(fig, master=tab2)
canvas.get_tk_widget().place(x=10,y=5)

# Create an animation to update the graphs
ani = animation.FuncAnimation(fig, update_graphs, interval=1000)


update_camera()
window.mainloop()