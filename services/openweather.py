import http
import httpx
import os
from fastapi.exceptions import HTTPException
from main import api_key, api_key_history

from httpx import Response


async def get_weather(
    city: str,
    country: str,
):
    units = "metric"
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city+","+country}&appid={api_key}&units={units}'
        )
        if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
            raise HTTPException(response.status_code, detail=response.text)
        return response.json()


async def get_history(city: str, country: str, start: str, end: str):
    units = "metric"
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(
            f'https://history.openweathermap.org/data/2.5/history/city?q={city+","+country}&type=hour&appid={api_key_history}&units={units}&start={start}&end={end}&cnt=1'
        )
        if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
            raise HTTPException(response.status_code, detail=response.text)
        return response.json()


async def get_forecast(city: str, country: str, after: str):
    units = "metric"
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(
            f'https://api.openweathermap.org/data/2.5/forecast/daily?q={city+","+country}&appid={api_key}&units={units}&cnt={after}'
        )
        if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
            raise HTTPException(response.status_code, detail=response.text)
        return response.json()
