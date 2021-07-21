import tkinter as tk
from tkinter import ttk

# main window
window = tk.Tk()
window.title('Growing Degrees Day Simulator')   
window.geometry('800x800')

# row configuration
rows = 0
while rows < 50:
    window.rowconfigure(rows, weight=1)
    window.columnconfigure(rows, weight=1)
    rows += 1

# style
style = ttk.Style()
style.configure("TNotebook", background="grey")     # Just to make it easier to see.
style.configure("TFrame", background="#fff")
    
# parent tab
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

#location section
loc=Label(tab1, text="Location").place(x=500, y=160)
location=Button(tab1, text="Location", width=10, height=2).place(x=500, y=185)
map_button=Button(tab1, text="Map", width=10, height=2).place(x=500, y=225)

# date selection
planting_date=Label(tab1, text="Planting Date").place(x=500, y=100)
date = ttk.Spinbox(tab1, from_=1, to=31, width=5).place(x=500, y=130)
tk.Label(tab1,text="date").place(x=550,y=130)
month = ttk.Spinbox(tab1, from_=1, to=12, width=5).place(x=580,y=130)
tk.Label(tab1,text="Month").place(x=630,y=130)

array=[]
for i in range(1970,2023,1):
    array.append(i)

combo = ttk.Combobox(tab1,width=5)
combo['values']=array
combo.current(0)
combo.place(x=673, y=130)

tk.Label(tab1,text="Year").place(x=730, y=130)


# temperature selection
def update_temp(value=None):
    text = f'{slider.get()} / 50'
    tk.Label(tab1, text=text).place(x=700, y=470)

# tk.Label(tab1, text="Base Temperature").grid(row=30, column=30)

tk.Label(tab1, text="Base Temperature (F)").place(x=600, y=400)

# command updates the value as slider toggles left or right
slider = tk.Scale(window, from_=30, to=50, orient=tk.HORIZONTAL, showvalue=0, command=update_temp)
slider.place(x=600, y=470)

# starting the program
window.mainloop()



#left_frame = tk.Frame(tab1).pack(side="left")
#right_frame = tk.Frame(tab1).pack(side = "right")
#top_frame = tk.Frame(tab1).pack()
#bottom_frame = tk.Frame(tab1).pack(side = "bottom")
