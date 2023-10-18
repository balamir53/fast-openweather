import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta

from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from sql_app.models import City, Weather

from dotenv import load_dotenv
# load environment variables from .env file

load_dotenv()

api_key = os.getenv("API_KEY")
api_key_history = os.getenv("API_KEY_HISTORY")

from services.openweather import get_weather, get_history, get_forecast
from sql_app import crud, models, schemas
from tools import convertCelsiustoFahrenheit, convertFahrenheittoCelsius

from sql_app.crud import create_city, get_city,create_weather, get_weather_data, create_weather
from sql_app import schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# retrieve database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_main():
    return {"msg": "Weather API"}


@app.get("/api/weather/{city}")
async def weather(
    city: str,
    country: str = "US",
    before: int = None,
    after: int = None,
    db: Session = Depends(get_db),
):
    # get the city from database, if there is none create it
    my_city = get_city(db, city)
    if not my_city :
        my_city = create_city(db,schemas.City(name=city))

    my_weather_data = []
    # no before and after is provided, respond current weather
    if not before and not after:
        # check the database first
        # my_weather = get_weather_data(db,my_city,datetime.now().strftime("%Y-%m-%d"))
        my_weather = get_weather_data(db,my_city,datetime.strptime(datetime.now().strftime("%Y-%m-%d"),"%Y-%m-%d"))
        if not my_weather:
            response = await get_weather(city, country)
            response = response["main"]
            new_data = {}
            new_data = {
                "date": datetime.strptime(datetime.now().strftime("%Y-%m-%d"),"%Y-%m-%d"),
                "temp": response["temp"],
                "temp_fahr": convertCelsiustoFahrenheit(response["temp"]),
                "owner_city": my_city.id,
            }

            my_weather_data.append(schemas.Weather(**new_data))
            # write to the database if not its there
            return create_weather(db,my_weather_data)
        else:
            my_weather_data.append(my_weather)
        
        return my_weather_data

    # check if they are above 7
    if (before and before > 7) or (after and after > 7):
        raise HTTPException(
            500, detail="API only returns 7 days earlier data and 7 day forecast "
        )

    response = {}
    # given there is a before
    if before:

        start = datetime.now() - timedelta(days=before)
        start = int(start.timestamp())
        history = await get_history(
            city, country, start, end=int(datetime.now().timestamp())
        )

        # return response
        response["history"] = history["list"]

    if after:
        forecast = await get_forecast(city, country, after)
        response["forecast"] = forecast["list"]

    return response
