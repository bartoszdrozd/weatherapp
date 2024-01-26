import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    feels_like: int
    temperature: int
    pressure: int
    humidity: int
    name: str
    country: str
    wind_speed: int
    timestamp: int
    timezone: int
    sunrise: int
    sunset: int
    #maybe wind_direction?

@dataclass
class ForecastData:
    temp_list: list
    icon_list: list
    timestamps: list


def get_lat_lon(city_name, API_key):
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_key}'
        ).json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    name, country = data.get('name'), data.get('country')
    return lat, lon, name, country

def get_current_weather(lat, lon, name, country, API_key):
    resp = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp')),
        feels_like=int(resp.get('main').get('feels_like')),
        pressure=int(resp.get('main').get('pressure')),
        humidity=int(resp.get('main').get('humidity')),
        wind_speed=int(resp.get('wind').get('speed')),
        timestamp=int(resp.get('dt')),
        timezone=int(resp.get('timezone')),
        sunrise=int(resp.get('sys').get('sunrise')),
        sunset=int(resp.get('sys').get('sunset')),
        name=name,
        country=country
    )
    return data

def get_weather_forecast(lat, lon, API_key):
    resp = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    forecast_data = ForecastData(
        temp_list = [int(item.get('main').get('temp')) for item in resp.get('list') if '12:00:00' in item['dt_txt']],
        icon_list = [item.get('weather')[0].get('icon') for item in resp.get('list') if '12:00:00' in item['dt_txt']],
        timestamps = [int(item.get('dt')) for item in resp.get('list') if '12:00:00' in item['dt_txt']]
    )

    return forecast_data

def main(city_name):
    lat, lon, name, country = get_lat_lon(city_name, api_key)
    weather_data = get_current_weather(lat, lon, name, country, api_key)
    forecast_data = get_weather_forecast(lat, lon, api_key)
    date_time = [datetime.fromtimestamp(weather_data.timestamp), datetime.fromtimestamp(weather_data.sunrise), datetime.fromtimestamp(weather_data.sunset)]
    return weather_data, forecast_data, date_time

if __name__ == "__main__":
    lat, lon, name, country = get_lat_lon('Boston', api_key)
    print(get_current_weather(lat, lon,name, country, api_key))
    print(get_weather_forecast(lat, lon, api_key))

