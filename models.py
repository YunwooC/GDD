from gui.database import Base
from sqlalchemy import Column, String, Integer, Float
import pickle
import pandas as pd


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    neighbourhood = Column(String(25))
    room_type = Column(String(25))
    minimum_nights = Column(Float())
    voyageurs = Column(Float())
    chambres = Column(Float())
    lits = Column(Float())
    salle_de_bains = Column(Float())
    prediction = Column(Float())


class Regressor(object):
    def __init__(self, path: str) -> None:
        self.path = path
        self.load()

    def load(self):
        with open(self.path, "rb") as model:
            self.model = pickle.load(model)

    def predict(self, data: pd.DataFrame):
        prediction = self.model.predict(data)
        return prediction
