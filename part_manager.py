import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# main window
window = tk.Tk()
window.title('Growing Degrees Day Simulator')
window.configure(bg='white')
window.geometry('800x600')

# row configuration
rows = 0
while rows < 40:
    window.rowconfigure(rows, weight=1)
    window.columnconfigure(rows, weight=1)
    rows += 1

# style
style = ttk.Style()
style.theme_use('clam')#'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
style.configure("TNotebook", background="white")
style.configure("TFrame", background="white")
style.configure("TLabel", foreground="#254647", background="white")

#title
title=ttk.Label(window, text ="Growing Degree Day Simulator",font=("Arial Bold",30), padding=20)
title.pack(side='top')

# parent tab
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

# two tabs
tabControl.add(tab1, text ='Graph')
tabControl.add(tab2, text ='How To use')
tabControl.pack(expand = 1, fill ="both")

ttk.Label(tab1, 
    text ="GDD Graph",font=("Arial Bold",30)).place(x=30, y=20)
ttk.Label(tab2,
    text ="Tutorial",font=("Arial Bold",30)).grid(column = 0,
                                    row = 10, 
                                    padx = 30,
                                    pady = 30)

# Graph Placement
# a canvas for placeholder. Modify to reflect the design
canvas = tk.Canvas(tab1, width=500,height=320)
canvas.place(x=30, y=90)

# date selection
ttk.Label(tab1, text="Planting Date", font=(14)).place(x=560, y=100)
date = ttk.Spinbox(tab1, from_=1, to=31, width=5).place(x=560, y=152)
ttk.Label(tab1,text="Date",font=("Arial",11)).place(x=560,y=130)
month = ttk.Spinbox(tab1, from_=1, to=12, width=5).place(x=623,y=152)
ttk.Label(tab1,text="Month",font=("Arial",11)).place(x=623,y=130)

array=[]
for i in range(1970,2023,1):
    array.append(i)

combo = ttk.Combobox(tab1,width=5)
combo['values']=array
combo.current(0)
combo.place(x=686, y=152)

ttk.Label(tab1,text="Year",font=("Arial",11)).place(x=686, y=130)

#location section
ttk.Label(tab1, text="Location", font=(14)).place(x=560, y=210)
location = tk.Button(tab1, text="Location", width=25,bg='#BCD9DA', relief='flat')
location.place(x=560, y=242)
map_button = tk.Button(tab1, text="Map", width=25,bg='#BCD9DA', relief='flat')
map_button.place(x=560, y=275)



# temperature selection
def update_temp(value=None):
    text = f'{int(slider.get())}'
    ttk.Label(tab1, text=text).place(x=707, y=370)


ttk.Label(tab1, text="Base Temperature (F)", font=(14)).place(x=560, y=330)
# command updates the value as slider toggles left or right
slider = ttk.Scale(tab1, from_=30, to=50, orient=tk.HORIZONTAL, length=136, command=update_temp)
slider.place(x=560, y=370)
ttk.Label(tab1, text='30 / 50').place(x=707, y=370)    # for default value

#open the info box
def onClick():
    tk.messagebox.showinfo("What is GDD?",  "In the absence of extreme conditions such as unseasonal drought or disease,"
 " plants grow in a cumulative stepwise manner which is strongly influenced by the ambient temperature."
 " Growing degree days take aspects of local weather into account and allow gardeners to predict "
 " (or, in greenhouses, even to control) the plants' pace toward maturity. source:wikipedia")

#info button
infobutton = tk.Button(window, text="More Info", command=onClick, height=2, width=10,font=(14),bg='#BCD9DA')
#infobutton.grid(row=window.grid_size()[1], column=window.grid_size()[0])
infobutton.pack(side='bottom')

# starting the program
window.mainloop()








#left_frame = tk.Frame(tab1).pack(side="left")
#right_frame = tk.Frame(tab1).pack(side = "right")
#top_frame = tk.Frame(tab1).pack()
#bottom_frame = tk.Frame(tab1).pack(side = "bottom")
