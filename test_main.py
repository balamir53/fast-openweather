from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_weather():
    response = client.get("api/weather/california")
    assert response.status_code == 200


def test_another_city():
    response = client.get("api/weather/istanbul?country=tr")
    assert response.status_code == 200


def test_history():
    response = client.get("api/weather/ankara?country=tr&before=4")
    assert response.status_code == 200


def test_forecast():
    response = client.get("api/weather/london?country=uk&after=2")
    assert response.status_code == 200


def test_time_interval_fail():
    reponse = client.get("api/weather/berlin?country=gr&before=9")
    assert reponse.status_code == 500


def test_history_forecast():
    response = client.get("api/weather/texas?before=7&after=7")
    assert response.status_code == 200
