import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

# main window
window = tk.Tk()
window.title('Growing Degrees Day Simulator')   
window.geometry('800x800')

rows = 0
while rows < 50:
    window.rowconfigure(rows, weight=1)
    window.columnconfigure(rows, weight=1)
    rows += 1

tabControl = ttk.Notebook(window)
tabControl.grid(row=10,column=0, columnspan=50, rowspan=49)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
# two tabs
tabControl.add(tab1, text ='Graph')
tabControl.add(tab2, text ='How To use')
tabControl.pack(expand = 1, fill ="both")

ttk.Label(tab1, 
    text ="GDD Graph",font=("Arial Bold",30)).grid(column = 0, 
                               row = 10,
                               padx = 30,
                               pady = 30)  
ttk.Label(tab2,
    text ="Tutorial",font=("Arial Bold",30)).grid(column = 0,
                                    row = 10, 
                                    padx = 30,
                                    pady = 30)


date = Spinbox(tab1, from_=1, to=31, width=5).grid(row=11,column=10)
tk.Label(tab1,text="date").grid(row=11,column=16)
month = Spinbox(tab1, from_=1, to=12, width=5).grid(row=11,column=21)
tk.Label(tab1,text="Month").grid(row=11,column=28)

array=[]
for i in range(2000,2023,1):
    array.append(i)

combo = Combobox(tab1,width=5)
combo['values']=array
combo.current(0)
combo.grid(row=11, column=33)

tk.Label(tab1,text="Year").grid(row=11,column=38)

# starting the program
window.mainloop()



#left_frame = tk.Frame(tab1).pack(side="left")
#right_frame = tk.Frame(tab1).pack(side = "right")
#top_frame = tk.Frame(tab1).pack()
#bottom_frame = tk.Frame(tab1).pack(side = "bottom")
