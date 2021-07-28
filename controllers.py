from gui.views import Form, View, Table
import tkinter.messagebox as tkmsg
from gui.models import Regressor, Prediction
import pandas as pd
from abc import ABC, abstractmethod
from gui.database import get_db


class Controller(ABC):
    @abstractmethod
    def bind(view: View):
        raise NotImplementedError


class PredictController(Controller):
    def __init__(self, model: Regressor) -> None:
        self.model = model
        self.view = None
        self.db = get_db()
        self.neighbourhoods = [
            "Entrepôt",
            "Hôtel-de-Ville",
            "Opéra",
            "Ménilmontant",
            "Louvre"
        ]
        self.room_types = [
            "Entire home/apt" "Private room",
            "Shared room",
            "Hotel room",
        ]
        self.entries_values = {}

    def bind(self, view: Form):
        self.view = view
        self.view.create_view(self.neighbourhoods, self.room_types)
        self.view.buttons["Valider"].configure(command=self.predict)

    def validate_entries(self):
        isvalid = True
        for key, item in self.view.entries.items():
            value = float(item.get())
            if value <= 0:
                tkmsg.showerror(
                    title="Validation error", message=f"{key}: can not be less than 0"
                )
                isvalid = False
            else:
                self.entries_values[key] = value
        return isvalid

    def validate_comboboxes(self):
        isvalid = True
        for key, item in self.view.comboboxes.items():
            value = item.get()
            if not value:
                tkmsg.showerror(
                    title="Validation error", message=f"{key}: can not be empty"
                )
                isvalid = False
        return isvalid

    def predict(self):
        if self.validate_entries() and self.validate_comboboxes():
            data = pd.DataFrame(
                {
                    "neighbourhood": [self.view.comboboxes["Neighbourhood"].get()],
                    "room_type": [self.view.comboboxes["Room type"].get()],
                    "minimum_nights": [self.entries_values["Minimum night"]],
                    "guests": [self.entries_values["Guests"]],
                    "rooms": [self.entries_values["Bedrooms"]],
                    "beds": [self.entries_values["Beds"]],
                    "bathrooms": [self.entries_values["Bath rooms"]],
                }
            )
            prediction = self.model.predict(data)[0]

            data = data.to_dict(orient="records")[0]
            data["prediction"] = prediction

            to_store = Prediction(**data)
            self.db.add(to_store)
            self.db.commit()
            tkmsg.showinfo(
                "Prediction",
                message=f'Your {self.view.comboboxes["Room type"].get()}  located at {self.view.comboboxes["Neighbourhood"].get()} is estimated at {round(prediction, 2)}$/night',
            )


class TableController(Controller):
    def __init__(self) -> None:
        super().__init__()
        self.db = get_db()
        self.view = None

    def bind(self, view: Table):
        self.view = view
        data = self.get_all_prediction()
        self.view.create_view(data)
        self.view.button.configure(command=self.update)

    def update(self):
        data = self.get_all_prediction()
        self.view.create_view(data)

    def get_all_prediction(self):
        data = self.db.query(Prediction).all()
        results = []
        sample = data[0]
        headers = list(sample.__dict__.keys())[1:]
        results.append(headers)
        for d in data:
            d.__dict__.pop("_sa_instance_state")
            headers = list(d.__dict__.keys())
            row = list(d.__dict__.values())
            results.append(row)
        return results
