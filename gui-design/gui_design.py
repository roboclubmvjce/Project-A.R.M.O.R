import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tkb

window = tk.Tk()
window.title('Project A.R.M.O.R') #window name
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry('%dx%d'%(width,height)) #dimensions of window
style = tkb.Style('darkly') #window theme


window.mainloop()
