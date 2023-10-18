from typing import List, Union
import datetime
from pydantic import BaseModel


class Weather(BaseModel):
    # description: str
    date: datetime.datetime
    temp: float
    temp_fahr : float

    owner_city: int


class City(BaseModel):
    name: str
    weathers: List[Weather] = []
