import tkinter as tk
from datetime import datetime
from meteostat import Point, Daily
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter import messagebox
import matplotlib.patches as mpatches
import csv

class Model():
    def __init__(self):
        pass

    def make_data(self, coordinates):
        # Get daily data
        self.coordinates = coordinates
        self.latitude = self.coordinates[0]
        self.longitude = self.coordinates[1]
        self.location = Point(self.latitude, self.longitude)
        self.data1 = Daily(self.location, datetime(2020, 1, 1), datetime(2020, 12, 31))
        self.data1 = self.data1.fetch()
        self.data1=self.data1[['tavg', 'tmin', 'tmax']]


class View():

    def set_style(self):
        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure("TNotebook", background="white")
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", foreground="#254647", background="white")

    def __init__(self, master):

        # style
        self.set_style()

        # title
        self.title = ttk.Label(master, text='Growing degree Day Simulator', font=('Arial Bold', 30), padding=20)
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

        # Graph Placement
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.location = Point(49.2497, -123.1193)
        self.data1 = Daily(self.location, datetime(2020, 1, 1), datetime(2020, 12, 31))
        self.data1 = self.data1.fetch()
        self.data1=self.data1[['tavg', 'tmin', 'tmax']]
        self.fig.add_subplot(111).plot(self.data1)
        
        #Legend
        self.avg_patch = mpatches.Patch(color='#2b7a78', label='avg temp')
        self.min_patch = mpatches.Patch(color='#3aafa9', label='min temp')
        self.max_patch = mpatches.Patch(color='#def2f1', label='max temp')
        self.gdd_patch = mpatches.Patch(color='red', label='gdd')
        self.fig.legend(handles=[self.avg_patch, self.min_patch, self.max_patch, self.gdd_patch], 
                        bbox_to_anchor=(0.128, 0.93, 1, 0), loc=2, ncol=4, borderaxespad=0, fontsize=7, edgecolor="white")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab1)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=20, y=58)

        # date selection
        self.dateselection = DateSelection(self.tab1)

        # location selection
        self.location = TypeSearch(self.tab1)

        # temperature selection
        # self.temperature = TemperatureSelection(self.tab1)

        def update_temp(value=None):
            text = f'{int(self.slider.get())}'
            ttk.Label(self.tab1, text=text).place(x=707, y=250)

        ttk.Label(self.tab1, text="Base Temperature (F)", font=(14)).place(x=560, y=210)
        # command updates the value as slider toggles left or right
        self.slider = ttk.Scale(self.tab1, from_=30, to=50, orient=tk.HORIZONTAL, length=136, command=update_temp)
        self.slider.place(x=560, y=250)
        ttk.Label(self.tab1, text='30 / 50').place(x=707, y=250)  # for default value

        # update function
        def click():
            pass
        # update button
        self.upbutton = tk.Button(self.tab1, text="Update", height=1, width=8, bg='#BCD9DA', pady=5)
        self.upbutton.place(x=30, y=450)

        # reset function
        def clicked():
            pass
        # reset button
        self.upbutton = tk.Button(self.tab1, text="Reset", command=clicked, height=1, width=8, bg='#BCD9DA', pady=5)
        self.upbutton.place(x=100, y=450)

        # open the info box
        def onClick():
            tk.messagebox.showinfo("What is GDD?",
                                   "In the absence of extreme conditions such as unseasonal drought or disease,"
                                   " plants grow in a cumulative stepwise manner which is strongly influenced by the ambient temperature."
                                   " Growing degree days take aspects of local weather into account and allow gardeners to predict "
                                   " (or, in greenhouses, even to control) the plants' pace toward maturity. source:wikipedia")

        # info button
        self.infobutton = tk.Button(master, text="More Info", command=onClick, height=1, width=8, bg='#BCD9DA', pady=5)
        # self.infobutton.grid(row=master.grid_size()[1], column=master.grid_size()[0],sticky='se')
        self.infobutton.pack(side='bottom')

        # How to Use Tab
        self.instructions = tk.Label(self.tab2,
                                     text="Welcome to the GDD Simulator! This app has GDD data from 1970 to 2021.\n"
                                          " To find the GDD, only three pieces of information are needed: planting date, location, and base"
                                          " temperature. \n Select the date and click on the location/map tab and select the location you want to calculate the"
                                          " GDD for. \n Then use the slider to select the base temperature. Once all three pieces of information\n"
                                          " are inputted, the graph will appear containing the average temperature and the GDD \n \n \n \n \n \n \n \n"
                                          " GDD is the base temperature subtracted from the sum of the maximum \n"
                                          " temperature and the minimum temperature divided by two. "
                                          "Click the more information tab for more information on GDD.",
                                     bg="white").place(x=30, y=100)


class DateSelection():
    def __init__(self, master):
        ttk.Label(master, text="Planting Date", font=(14)).place(x=560, y=100)

        self.dateselection = ttk.Spinbox(master, from_=1, to=31, width=5).place(x=560, y=152)
        ttk.Label(master, text="Date", font=('Arial', 11)).place(x=560, y=130)
        self.monthselection = ttk.Spinbox(master, from_=1, to=12, width=5).place(x=623, y=152)
        ttk.Label(master, text="Month", font=('Arial', 11)).place(x=623, y=130)

        self.array2 = []
        for i in range(1970, 2023, 1):
            self.array2.append(i)
        self.yearselection = ttk.Combobox(master, width=5)
        self.yearselection['values'] = self.array2
        self.yearselection.current(0)
        self.yearselection.place(x=686, y=152)

        ttk.Label(master, text="Year", font=("Arial", 11)).place(x=686, y=130)

    def get_date(self):
        self.date = self.dateselection.get()
        self.month = self.monthselection.get()
        self.year = self.yearselection.get()

        return [self.date, self.month, self.year]


class TypeSearch():
    def __init__(self, master):

        ttk.Label(master, text="Location", font=(14)).place(x=560, y=280)

        # Create an entry box
        self.my_entry = tk.Entry(master, width=25)
        self.my_entry.place(x=560, y=320)

        # Create a listbox
        self.my_list = tk.Listbox(master, width=25)

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

    # returns the x and y dimension of the city
    def get_location(self):
        self.coordinates = []

        with open('uscities.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.my_entry.get() == row['city']:
                    self.coordinates = [float(row['lat']), float(row['lng'])]

        if self.coordinates is None or len(self.coordinates) < 2:
            print("No location found; default coordintes: (49.2497, -123.1193)")
            return [49.2497, -123.1193]
        else:
            return self.coordinates


    def show_listbox(self, e):
        self.my_list.place(x=560, y=335)

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
        self.view = View(self.root)
        # self.view.upbutton.bind("<Button-1>", self.create_plot)

    # to check if get_location()'s working
    #     def checking(self):
    #         if self.view.location.called:
    #             print(self.view.location.get_location())

    #         self.root.after(5000, self.checking)

    def run(self):
        self.root.title("Growing degree Day Simulator")
        self.root.configure(bg='white')
        self.root.minsize(800, 650)
        self.root.deiconify()

        # self.root.after(5000, self.checking)

        self.root.mainloop()


if __name__ == '__main__':
    c = Controller()
    c.run()
