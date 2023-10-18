from sqlalchemy.orm import Session
from datetime import datetime,timedelta
from typing import List

from . import models, schemas


def create_city(db: Session, city: schemas.City):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    return db_city

def get_city(db: Session, city: str):
    if db.query(models.City).filter(models.City.name == city).first():
        return db.query(models.City).filter(models.City.name == city).first()
    return None
    # return db.get_or_404(models.City.name == city)
def get_cities(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.City).offset(skip).limit(limit).all()

def create_weather(db: Session, weather:List[schemas.Weather]):
    # take the list, iterate it and write it to the database
    db_weather_list = []
    for weat in weather:
        db_weather = models.Weather(**weat.dict())
        db.add(db_weather)
        db_weather_list.append(db_weather)
    db.commit()
    return weather

def get_weathers_data(db : Session, city: schemas.City):
    return db.query(models.Weather).filter(models.Weather.owner_city == city.id)

def get_weather_data(db:Session, city:models.City, date: datetime):
    # date = datetime.strptime(date,"%Y-%m-%d")
    if db.query(models.Weather).filter(models.Weather.date==date).filter(models.Weather.owner_city==city.id).first():
        return db.query(models.Weather).filter(models.Weather.date==date).filter(models.Weather.owner_city==city.id).first()