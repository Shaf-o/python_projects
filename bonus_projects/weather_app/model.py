import json
from datetime import datetime as dt
from dataclasses import dataclass
from typing import Final
import requests

# Constants
API_KEY: Final[str] = 'YOUR_KEY'
BASE_URL: Final[str] = 'https://api.openweathermap.org/data/2.5/forecast'


@dataclass
class Weather:
    date: dt
    details: dict
    temp: str
    weather: list[dict]
    description: str

    def __str__(self):
        return f'[{self.date:%H:%M}] {self.temp}C° ({self.description})'


def get_weather(city_name: str, mock: bool = True) -> dict:
    """Gets the current weather from the weather api"""

    # Return dummy data for testing
    if mock:
        with open('dummy_data.json') as file:
            return json.load(file)

    # Request live data
    payload: dict = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    request = requests.get(url=BASE_URL, params=payload)
    data: dict = request.json()

    return data


def get_weather_details(weather: dict) -> list[Weather]:
    """Takes the weather json and turns it into a nice list of Weather objects"""

    days: list[dict] = weather.get('list')

    # If there is no data for days, no point in continuing
    if not days:
        raise Exception(f'Problem with json: {weather}')

    # Try to add the info we want to our list_of_weather
    list_of_weather: list[Weather] = []
    for day in days:
        w: Weather = Weather(date=dt.fromtimestamp(day.get('dt')),
                             details=(details := day.get('main')),
                             temp=details.get('temp'),
                             weather=(weather := day.get('weather')),
                             description=weather[0].get('description'))
        list_of_weather.append(w)

    return list_of_weather
