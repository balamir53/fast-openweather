from typing import List
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta

from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session

from dotenv import load_dotenv

from services.openweather import get_weather, get_history, get_forecast
from sql_app import crud, models, schemas

# load environment variables from .env file
load_dotenv()

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
    return{"msg":"Weather API"}

@app.get("/api/weather/{city}")
async def weather(
    city :str,
    country : str = "US",
    units : str = "metric",
    before : int = None,
    after : int = None,
    db : Session = Depends(get_db)
):
    # no before and after is provided, respond current weather
    if not before and not after:
        response = await get_weather(city,country,units)
        return response['main']
    
    # check if they are above 7
    if (before and before > 7) or (after and after > 7):
        raise HTTPException (500, detail="API only returns 7 days earlier data and 7 day forecast ")
    
    response = {}
    # given there is a before
    if before:
        start = datetime.now()-timedelta(days=before)
        start = int(start.timestamp())
        history = await get_history(city,country,units,start,end=int(datetime.now().timestamp()))
        # return response
        response["history"] = history["list"]
    
    if after:
        forecast = await get_forecast(city,country,units,after)
        response["forecast"] = forecast["list"]

    return response
         
