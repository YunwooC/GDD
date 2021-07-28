import tkinter as tk
from gui.controllers import Controller, PredictController, TableController
from gui.views import Form, Table
from gui.models import Regressor
from tkinter import ttk
from gui.database import Base, engine


class Application(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    def new_tab(self, controller: Controller, view: Form, name: str):
        view = view(self.master)
        controller.bind(view)
        self.add(view, text=name)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    Base.metadata.create_all(engine, checkfirst=True)

    app = Application(master=root)

    regressor = Regressor("airbnb_regressor.pickle")
    predict_controller = PredictController(model=regressor)
    table_controller = TableController()

    app.new_tab(view=Form, controller=predict_controller, name="Prediction")
    app.new_tab(view=Table, controller=table_controller, name="Table")

    app.mainloop()
