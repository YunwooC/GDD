import tkinter as tk
from tkinter import ttk
from abc import abstractmethod
from typing import List
from tkinter import messagebox

class View(tk.Frame):
    @abstractmethod
    def create_view(self):
        raise NotImplementedError

class Form(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.entries = {}
        self.buttons = {}
        self.comboboxes = {}
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_view(self):

        control_frame = tk.LabelFrame(master=self, text="Input data")
        control_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(0, weight=1)
        control_frame.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)


        # date selection
        array = []
        for i in range(1970, 2023, 1):
            array.append(i)

        self.create_combobox(control_frame, "Year", x=686, y=152, values=array)


        # location selection
        # self.create_button(control_frame, "Valider", row=3, column=0)


        # temperature selection


        # info button



    def create_button(self, frame, name, x, y):
        self.buttons[name] = tk.Button(frame)
        self.buttons[name]["text"] = name
        self.buttons[name].place(x=x, y=y)

    def create_combobox(self, frame, label, values, x, y):
        label_frame = tk.LabelFrame(frame, text=label)
        self.comboboxes[label] = ttk.Combobox(label_frame, values=values)
        self.comboboxes[label].grid(row=1, column=1)
        label_frame.place(x=x, y=y)

    def create_Label(self, frame, text, x, y):
        # to be implemented
        return

    def create_Scale(self, frame, from_, to, orient, length, command):
        # to be implemented
        return

class Table(View):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_button()

    def create_view(self, data: List):
        frame = tk.Frame(self)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        total_rows = len(data)
        total_columns = len(data[0])
        for row in range(total_rows):
            for col in range(total_columns):
                entry = tk.Entry(
                    frame,
                    width=10,
                )

                entry.grid(row=row, column=col, sticky=tk.N + tk.S + tk.E + tk.W)
                entry.rowconfigure(0, weight=1)
                entry.columnconfigure(0, weight=1)
                entry.insert(tk.END, data[i][j])

    def create_button(self):
        frame = tk.Frame(self)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        self.button = tk.Button(frame)
        self.button["text"] = "refresh"
        self.button.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        frame.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
