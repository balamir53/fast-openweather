from typing import List, Union
import datetime
from pydantic import BaseModel


class Weather(BaseModel):
    # description: str
    date: datetime.datetime
    country: str
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int

    owner_city: int


class City(BaseModel):
    name: str
    reports: List[Weather] = []
