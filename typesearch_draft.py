from tkinter import *
import csv

class TypeSearch():
    def __init__(self, master):

        self.my_label = Label(master, text='Start Typing...', fg='grey')
        self.my_label.pack(pady=20)

        # Create an entry box
        self.my_entry = Entry(master, font=("Helvetica", 20))
        self.my_entry.pack()

        # Create a listbox
        self.my_list = Listbox(master, width=50)
        self.my_list.pack(pady=40)

        # read in the list of cities
        self.cities = []
        with open('uscities.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.cities.append(row['city'])

        self.update(self.cities)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

        master.mainloop()
        
    def getlocation(self):
        with open('uscities.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.my_entry.get() == row['city']:
                    return [row['lat'], row['lng']]

    def fillout(self, e):
        # Delete whatever is in the entry box
        self.my_entry.delete(0, END)

        # Add clicked list item to entry box
        self.my_entry.insert(0, self.my_list.get(ANCHOR))

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
        self.my_list.delete(0, END)

        # Add toppings to listbox
        for item in data:
            self.my_list.insert(END, item)

root = Tk()
root.title('test')
root.geometry("500x300")

t = TypeSearch(root)
