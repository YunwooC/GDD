import tkinter as tk
from datetime import datetime, timedelta
from meteostat import Point, Daily
import matplotlib.style
from cycler import cycler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from tkinter import ttk
from tkinter import messagebox
import csv

class Model():
    def __init__(self):
        pass

    def make_data(self, coordinates, time, temperature):
        # Fetched data
        self.coordinates = coordinates
        self.time = time
        self.temperature = temperature

        self.latitude = self.coordinates[0]
        self.longitude = self.coordinates[1]
        self.location = Point(self.latitude, self.longitude)
        self.data1 = Daily(self.location, self.time[0],self.time[1])
        self.data1 = self.data1.fetch()

        # calculate gdd
        self.s = self.data1['tavg']
        self.GDD = [0]
        self.gdd = 0
        for i in range(210):
            self.avg = self.s[i]
            if self.avg <= self.temperature:
                g = 0
            else:
                g = self.avg - self.temperature
            self.gdd+=g
            self.GDD.append(self.gdd)
        self.data1["GDD"]=self.GDD
        self.data1 = self.data1[['tavg', 'tmin', 'tmax', "GDD"]]


class View():
    def __init__(self, master, controller):

        # style
        self.set_style()

        # title
        self.title = ttk.Label(master, text='Growing degree Day Simulator', font=('Times', 40), padding=20)
        self.title.pack(side='top')

        # parent tab
        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        # two tabs configuration
        self.tabControl.add(self.tab1, text='Graph')
        self.tabControl.add(self.tab2, text='How to Use')
        self.tabControl.pack(expand=1, fill='both')
        ttk.Label(self.tab1, text="GDD Graph", font=("Times", 30)).place(x=30, y=20)
        ttk.Label(self.tab2, text="Tutorial", font=("Times", 30)).place(x=30, y=20)

        # date selection
        self.dateselection = DateSelection(self.tab1)
        # location selection
        self.location = TypeSearch(self.tab1)
        # temperature selection
        self.temperature = TemperatureSelection(self.tab1)


        # update button
        self.upbutton = tk.Button(self.tab1, text="Update", relief=tk.FLAT, command=controller.make_graph, height=1, width=8, bg='#BCD9DA', pady=5)
        self.upbutton.place(x=30, y=430)

        # reset button
        self.rebutton = tk.Button(self.tab1, text="Reset", relief=tk.FLAT, command=controller.reset, height=1, width=8, bg='#BCD9DA', pady=5)
        self.rebutton.place(x=100, y=430)

        # open the info box
        def onClick():
            tk.messagebox.showinfo("What is GDD?",
                                   "In the absence of extreme conditions such as unseasonal drought or disease,"
                                   " plants grow in a cumulative stepwise manner which is strongly influenced by the ambient temperature."
                                   " Growing degree days take aspects of local weather into account and allow gardeners to predict "
                                   " (or, in greenhouses, even to control) the plants' pace toward maturity. source:wikipedia")

        # info button
        self.infobutton = tk.Button(master, text="More Info", command=onClick, relief=tk.FLAT, height=1, width=8, bg='#BCD9DA', pady=5)
        # self.infobutton.grid(row=master.grid_size()[1], column=master.grid_size()[0],sticky='se')
        self.infobutton.pack(side='bottom')

        # How to Use Tab
        self.instructions = tk.Label(self.tab2,
                                     text="Welcome to the GDD Simulator! This app has GDD data from 1970 to 2021.\n"
                                          " To find the GDD, only three pieces of information are needed: planting date, location, and base"
                                          " temperature. \n Select the date and click on the location/map tab and select the location you want to calculate the"
                                          " GDD for. \n Then use the slider to select the base temperature. Once all three pieces of information\n"
                                          " are inputted, click the update button and the graph will appear containing the average temperature and the GDD. \n" 
                                          " The reset button changes the planting date value to 01/01/2019, the base temperature to 10 degrees Celsius and"
                                          " the location to Vancouver. \n \n \n \n \n \n \n"
                                          " GDD is the base temperature subtracted from the sum of the maximum \n"
                                          " temperature and the minimum temperature divided by two. "
                                          "Click the more information tab for more information on GDD.",
                                     bg="white").place(x=30, y=100)

    # display graph on GUI
    def plot(self, data):
        self.fig = Figure(figsize=(5.2, 3.3), dpi=100)
        self.ax = self.fig.add_subplot(111).plot(data)

        # Legend
        self.avg_patch = mpatches.Patch(color='#2b7a78', label='avg temp')
        self.max_patch = mpatches.Patch(color='#3aafa9', label='max temp')
        self.min_patch = mpatches.Patch(color='#def2f1', label='min temp')
        self.gdd_patch = mpatches.Patch(color='red', label='gdd')
        self.fig.legend(handles=[self.avg_patch, self.max_patch, self.min_patch, self.gdd_patch],
                        bbox_to_anchor=(0.128, 0.93, 1, 0), loc=2, ncol=4, borderaxespad=0, fontsize=7,
                        edgecolor="white")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab1)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=20, y=70)

    def set_style(self):
        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure("TNotebook", background="white")
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", foreground="#254647", background="white", font=("Times"))
        self.style.configure("TSpinbox", fieldbackground="#EDEEF0", selectbackground="#3AAFA9")
        self.style.configure("TCombobox", fieldbackground="#EDEEF0", selectbackground="#3AAFA9", arrowcolor="#3AAFA9")
        self.style.configure("TEntry", foreground="#3AAFA9")
        self.style.configure("Horizontal.TScale", background="#EDEEF0", troughcolor="#EDEEF0", groovewidth=1)

        matplotlib.rcParams['font.size'] = 8
        matplotlib.rcParams['boxplot.boxprops.color'] = "#EDEEF0"
        matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['#2b7a78', '#def2f1', '#3aafa9', 'red', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
        matplotlib.rcParams['patch.edgecolor'] = '#EDEEF0'
        print(matplotlib.rcParams)

class TemperatureSelection():
    def __init__(self, master):
        self.master = master

        ttk.Label(master, text="Base Temperature (C)", font=("Times", 17)).place(x=560, y=210)
        self.slider = ttk.Scale(master, from_=10, to=50, orient=tk.HORIZONTAL, length=136, command=self.show_temp)
        self.slider.set(10)
        self.slider.place(x=560, y=250)

        # number display
        self.show_temp()

    def show_temp(self, value=None):
        text = f'{int(self.slider.get())} / 50'
        ttk.Label(self.master, text=text, font=("Times", 11), foreground="#3AAFA9").place(x=707, y=250)

    def get_temperature(self):
        self.temperature = self.slider.get()

        if self.temperature is None:
            print("Null")
            return

        return self.slider.get()

class DateSelection():
    def __init__(self, master):
        ttk.Label(master, text="Planting Date", font=("Times", 17)).place(x=560, y=100)

        # default date, month, and year
        self.date_default = tk.StringVar(master)
        self.date_default.set('1')
        self.month_default = tk.StringVar(master)
        self.month_default.set('1')
        self.year_default = tk.StringVar(master)
        self.year_default.set('2020')

        ttk.Label(master, text="Date", font=("Times", 11)).place(x=560, y=130)
        self.dateselection = ttk.Spinbox(master, from_=1, to=31, width=5)
        self.dateselection.set(1)
        self.dateselection.place(x=560, y=152)

        ttk.Label(master, text="Month", font=("Times", 11)).place(x=623, y=130)
        self.monthselection = ttk.Spinbox(master, from_=1, to=12, width=5)
        self.monthselection.set(1)
        self.monthselection.place(x=623, y=152)
        self.monthselection.set(1)

        ttk.Label(master, text="Year", font=("Times", 11)).place(x=686, y=130)
        self.array2 = []
        for i in range(1970, 2021, 1):
            self.array2.append(i)
        self.yearselection = ttk.Combobox(master, textvariable=self.year_default, width=5)
        self.yearselection['values'] = self.array2
        self.yearselection.current(50)
        self.yearselection.place(x=686, y=152)

    def get_date(self):
        self.date = int(self.dateselection.get())
        self.month = int(self.monthselection.get())
        self.year = int(self.yearselection.get())
        self.time=datetime(self.year,self.month,self.date)
        self.end_time=self.time + timedelta(days=210)

        return [self.time, self.end_time]

class TypeSearch():
    def __init__(self, master):

        ttk.Label(master, text="Location", font=("Times", 17)).place(x=560, y=290)

        # Create an entry box
        self.default = tk.StringVar(master, value="Vancouver")
        self.my_entry = tk.Entry(master, width=25, justify=tk.CENTER, textvariable=self.default, relief=tk.FLAT, bg="#EDEEF0", fg="#3AAFA9")
        self.my_entry.place(x=560, y=330)

        # Create a listbox
        self.my_list = tk.Listbox(master, width=25, selectbackground="#3AAFA9", height=5)

        # read in the list of cities
        self.cities = []
        with open('uscities.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.cities.append(row['city'])

        self.update(self.cities)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)
        self.my_entry.bind("<FocusIn>", self.show_listbox)
        self.my_entry.bind("<FocusOut>", self.hide_listbox)

    def is_no_location(self, coordinates):
        self.location = Point(coordinates[0], coordinates[1])
        self.meteostat = Daily(self.location, datetime(2020, 1, 1), datetime(2021, 1, 1))

        if self.meteostat.count() == 0:
            return True
        else:
            return False

    # returns the x and y dimension of the city
    def get_location(self):
        self.coordinates = []

        with open('uscities.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.my_entry.get() == row['city']:
                    self.coordinates = [float(row['lat']), float(row['lng'])]

        if self.coordinates is None or len(self.coordinates) < 2 or self.is_no_location(self.coordinates):
            tk.messagebox.showinfo("No location found.",
                                   "default location Vancouver")
            return [49.2497, -123.1193]
        else:
            return self.coordinates

    def show_listbox(self, e):
        self.my_list.place(x=560, y=345)

    def hide_listbox(self, e):
        self.my_list.place_forget()

    def fillout(self, e):
        # Delete whatever is in the entry box
        self.my_entry.delete(0, tk.END)

        # Add clicked list item to entry box
        self.my_entry.insert(0, self.my_list.get(tk.ANCHOR))
        self.called = True

    def check(self, e):
        # grab what was typed
        typed = self.my_entry.get()

        if typed == '':
            data = self.cities
        else:
            data = []
            for item in self.cities:
                if typed.lower() in item.lower():
                    data.append(item)

        # update our listbox with selected items
        self.update(data)

    def update(self, data):
        self.my_list.delete(0, tk.END)

        # Add toppings to listbox
        for item in data:
            self.my_list.insert(tk.END, item)


class Controller():
    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = View(self.root, controller=self)
        # initial graph
        self.make_graph()

    def make_graph(self):
        print("Graph Displayed")
        self.location_data = self.view.location.get_location()
        self.date_data = self.view.dateselection.get_date()
        self.temperature_data = self.view.temperature.get_temperature()

        self.model.make_data(self.location_data, self.date_data, self.temperature_data)
        self.data = self.model.data1
        self.view.plot(self.data)
        
    def reset(self):
        #Set to default values
        self.view.temperature.slider.set(10)
        self.view.temperature.show_temp()
        self.view.dateselection.dateselection.set(1)
        self.view.dateselection.monthselection.set(1)
        self.view.dateselection.yearselection.current(49)
        self.view.dateselection.get_date()
        
        self.base_temp=10
        self.default_date=datetime(2019,1,1)
        self.default_data=Daily(Point(49.2497,-123.1193), self.default_date, self.default_date + timedelta(days=210))
        self.default_data=self.default_data.fetch()
        self.v = self.default_data['tavg']
        self.dGDD = [0]
        self.dgdd = 0
        for i in range(210):
            self.davg = self.v[i]
            if self.davg <= self.base_temp:
                dg = 0
            else:
                dg = self.davg - self.base_temp
            self.dgdd+=dg
            self.dGDD.append(self.dgdd)
        self.default_data["GDD"]=self.dGDD
        self.default_data=self.default_data[['tavg','tmin','tmax','GDD']]
        self.view.plot(self.default_data)
        
    def run(self):
        self.root.title("Growing Degree Day Simulator")
        self.root.configure(bg='white')
        self.root.minsize(800, 650)
        self.root.deiconify()

        self.root.mainloop()

if __name__ == '__main__':
    c = Controller()
    c.run()
