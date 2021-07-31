import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

class Model():

    def __init__(self):
        self.xpoint = 200
        self.ypoint = 200
        self.res = None

    # def calculate(self):
    #     x, y = np.meshgrid(np.linspace(-5, 5, self.xpoint), np.linspace(-5, 5, self.ypoint))
    #     z = np.cos(x ** 2 * y ** 3)
    #     self.res = {"x": x, "y": y, "z": z}


class View():
    def __init__(self, master):
        self.frame = tk.Frame(master)

        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure("TNotebook", background="white")
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", foreground="#254647", background="white")
       
        # title
        self.title = ttk.Label(master, text='Growing degree Day Simulator', font=('Arial Bold',30), padding=20)
        self.title.pack(side='top')
        #self.title.grid(row=0,column=0,sticky='n')

        # parent tab
        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)

        # two tabs configuration
        self.tabControl.add(self.tab1, text='Graph')
        self.tabControl.add(self.tab2, text='How to Use')
        self.tabControl.pack(expand=1, fill='both')
        ttk.Label(self.tab1, text="GDD Graph", font=("Times",30)).place(x=30, y=20)
        ttk.Label(self.tab2, text="Tutorial", font=("Times",30)).place(x=30, y=20)

        # Graph Placement
        tk.Canvas(self.tab1, width=500, height=320).place(x=30, y=90)

        # date selection
        ttk.Label(self.tab1, text="Planting Date", font=(14)).place(x=560, y=100)
        self.date = ttk.Spinbox(self.tab1, from_=1, to=31, width=5).place(x=560, y=152)
        ttk.Label(self.tab1, text="Date",font=('Arial',11)).place(x=560, y=130)
        month = ttk.Spinbox(self.tab1, from_=1, to=12, width=5).place(x=623, y=152)
        ttk.Label(self.tab1, text="Month",font=('Arial',11)).place(x=623, y=130)

        array = []
        for i in range(1970, 2023, 1):
            array.append(i)

        self.combo = ttk.Combobox(self.tab1, width=5)
        self.combo['values'] = array
        self.combo.current(0)
        self.combo.place(x=686, y=152)

        ttk.Label(self.tab1,text="Year",font=("Arial",11)).place(x=686, y=130)

        # location selection
        ttk.Label(self.tab1, text="Location", font=(14)).place(x=560, y=290)
        self.location = TypeSearch(self.tab1)


        # temperature selection
        def update_temp(value=None):
            text = f'{int(self.slider.get())}'
            ttk.Label(self.tab1, text=text).place(x=707, y=250)


        ttk.Label(self.tab1, text="Base Temperature (F)", font=(14)).place(x=560, y=210)
        # command updates the value as slider toggles left or right
        self.slider = ttk.Scale(self.tab1, from_=30, to=50, orient=tk.HORIZONTAL, length=136, command=update_temp)
        self.slider.place(x=560, y=250)
        ttk.Label(self.tab1, text='30 / 50').place(x=707, y=250)    # for default value

        #open the info box
        def onClick():
            tk.messagebox.showinfo("What is GDD?",  "In the absence of extreme conditions such as unseasonal drought or disease,"
            " plants grow in a cumulative stepwise manner which is strongly influenced by the ambient temperature."
            " Growing degree days take aspects of local weather into account and allow gardeners to predict "
            " (or, in greenhouses, even to control) the plants' pace toward maturity. source:wikipedia")

        #info button
        self.infobutton = tk.Button(master, text="More Info", command=onClick, height=2, width=10, bg='#BCD9DA')
        #self.infobutton.grid(row=master.grid_size()[1], column=master.grid_size()[0],sticky='se')
        self.infobutton.pack(side='bottom')

        #How to Use Tab
        self.instructions=tk.Label(self.tab2, text="Welcome to the GDD Simulator! This app has GDD data from 1970 to 2021.\n"
                      " To find the GDD, only three pieces of information are needed: planting date, location, and base"
                      " temperature. \n Select the date and click on the location/map tab and select the location you want to calculate the"
                      " GDD for. \n Then use the slider to select the base temperature. Once all three pieces of information\n"
                      " are inputted, the graph will appear containing the average temperature and the GDD \n \n \n \n \n \n \n \n"
                      " GDD is the base temperature subtracted from the sum of the maximum \n"
                      " temperature and the minimum temperature divided by two. "
                      "Click the more information tab for more information on GDD.",bg="white").place(x=30, y=100)

class TypeSearch():
    def __init__(self, master):
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
    def getlocation(self):
        with open('uscities.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.my_entry.get() == row['city']:
                    return [row['lat'], row['lng']]

    def show_listbox(self, e):
        self.my_list.place(x=560, y=335)

    def hide_listbox(self, e):
        self.my_list.place_forget()

    def fillout(self, e):
        # Delete whatever is in the entry box
        self.my_entry.delete(0, tk.END)

        # Add clicked list item to entry box
        self.my_entry.insert(0, self.my_list.get(tk.ANCHOR))

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
        # self.view.sidepanel.plotBut.bind("&lt;Button&gt;", self.my_plot)
        # self.view.sidepanel.clearButton.bind("&lt;Button&gt;", self.clear)

    def run(self):
        self.root.title("Growing degree Day Simulator")
        self.root.configure(bg='white')
        self.root.geometry('800x650')
        self.root.deiconify()
        self.root.mainloop()

    # def clear(self, event):
    #     self.view.ax0.clear()
    #     self.view.fig.canvas.draw()
    #
    # def my_plot(self, event):
    #     self.model.calculate()
    #     self.view.ax0.clear()
    #     self.view.ax0.contourf(self.model.res["x"], self.model.res["y"], self.model.res["z"])
    #     self.view.fig.canvas.draw()


if __name__ == '__main__':
    c = Controller()
    c.run()
