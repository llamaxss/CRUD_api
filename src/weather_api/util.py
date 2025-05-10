from requests import Response, request
from flask import (
    jsonify,
)
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)


WEATHER_API = os.getenv("WEATHER_API")
GEOCODE_API = os.getenv("GEOCODE_API")
API_KEY = os.getenv("API_KEY")


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ResultWeather:
    def __init__(self, status, msg=None, country=None, feels_like=None, temp=None):
        self.status = status
        self.msg = msg
        self.country = country
        self.feels_like = feels_like
        self.temp = temp


def result_weather_mapper(result: Response) -> Response:

    try:
        result = result.json()
        country = result["sys"]["country"]
        feels_like_kelvin = result["main"]["feels_like"]
        temp_kelvin = result["main"]["temp"]

        feels_like_celsius = str((round(int(kelvin_to_celsius(feels_like_kelvin)), 2)))
        temp_celsius = str(round(int(kelvin_to_celsius(temp_kelvin)), 2))

    except KeyError as e:
        res = jsonify({"error": "Invalid response from weather API"})
        res.status_code = 500
        return res

    res = jsonify(
        {
            "country": country,
            "feels_like": feels_like_celsius,
            "temp": temp_celsius,
        },
    )
    res.status_code = 200
    return res


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def validate_geocode(lat: str, lon: str) -> None:
    if not lat or not lon:
        raise ValidationError("Latitude and Longitude are required")
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        raise ValidationError("Latitude and Longitude must be numbers")


def validate_city_name(city_name: str) -> None:
    if not city_name:
        raise ValidationError("City name is required")
    if not isinstance(city_name, str):
        raise ValidationError("City name must be a string")


def get_weather_data(lat, lon) -> Response:
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    res = request(method="GET", url=WEATHER_API, params=params)
    return res


def handle_weather_geocode(lat, lon) -> Response:

    try:
        validate_geocode(lat, lon)
    except ValidationError as e:
        res = jsonify({"error": str(e)})
        res.status_code = 400
        return res

    try:
        res = get_weather_data(lat, lon)
    except Exception as e:
        res = jsonify({"error": str(e)})
        res.status_code = 500
        return res

    return result_weather_mapper(res)


def handle_weather_city(city_name) -> Response:

    try:
        validate_city_name(city_name)
    except ValidationError as e:
        res = jsonify({"error": str(e)})
        res.status_code = 400
        return res

    params = {"q": city_name, "limit": 1, "appid": API_KEY}
    res = request(method="GET", url=GEOCODE_API, params=params)
    data = res.json()

    if not data:
        res = jsonify({"error": "City not found"})
        res.status_code = 404
        return res

    lat = data[0]["lat"]
    lon = data[0]["lon"]
    try:
        res = get_weather_data(lat, lon)
    except Exception as e:
        res = jsonify({"error": str(e)})
        res.status_code = 500
        return res

    return result_weather_mapper(res)
