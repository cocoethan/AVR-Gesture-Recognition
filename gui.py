import tkinter as tk
#import traceback
from tkinter import filedialog, LEFT, TOP
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox

#Set-up Window
window = tk.Tk()
window.title("AIVRGlove Interface")
window.geometry('565x505')
window.resizable(False, False)

frame_1 = tk.Frame(window)

menubar = tk.Menu(window)
helpMenu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label="Help", menu=helpMenu)
window.config(menu=menubar)

window.mainloop()