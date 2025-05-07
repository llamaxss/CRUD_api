from flask import Flask, jsonify, request, Response, render_template, redirect, url_for
import requests
import os

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


app = Flask(__name__)

WEATHER_API = os.getenv("WEATHER_API")
GEOCODE_API = os.getenv("GEOCODE_API")
API_KEY = os.getenv("API_KEY")


def fetch_data(api, params, method="GET") -> Response:
    response = requests.request(method=method, url=api, params=params)

    if response.status_code == 200:
        if not response.json():
            response = jsonify({"error": "No data found"})
            response.status_code = 404
            return response
        else:
            response = jsonify(response.json())
            response.status_code = 200
            return response
    else:
        response = jsonify({"error": "Failed to fetch data from the API"})
        response.status_code = 500
        return response


def get_weather(lat, lon) -> Response:
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    res = fetch_data(WEATHER_API, params)

    return res


def validate_city_name(city_name: str) -> None:
    if not city_name:
        raise ValidationError("City name is required")
    if not isinstance(city_name, str):
        raise ValidationError("City name must be a string")


@app.post("/weather/city")
def get_location_city_name():
    city_name = request.form.get("city-name")

    try:
        validate_city_name(city_name)
    except ValidationError as e:
        result = ResultWeather(status="error", msg=str(e))
        return render_template("index.html", result=result)
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY,
    }
    res = fetch_data(GEOCODE_API, params)
    if res.status_code != 200:
        result = ResultWeather(status="error", msg="City not found")
        return render_template("index.html", result=result)
    data = res.json
    lat = data[0]["lat"]
    lon = data[0]["lon"]

    weather_data = get_weather(lat, lon)

    result = result_weather_mapper(weather_data)
    return render_template(
        "index.html",
        result=result,
    )


def validate_geocode(lat: str, lon: str) -> None:
    if not lat or not lon:
        raise ValidationError("Latitude and Longitude are required")
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        raise ValidationError("Latitude and Longitude must be numbers")


@app.post("/weather/geocode")
def get_location_by_coordinates():
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    try:
        validate_geocode(lat, lon)
    except ValidationError as e:
        result = ResultWeather(status="error", msg=str(e))
        return render_template("index.html", result=result)

    weather_data = get_weather(lat, lon)

    result = result_weather_mapper(weather_data)
    return render_template(
        "index.html",
        result=result,
    )


class ResultWeather:
    def __init__(self, status, msg=None, country=None, feels_like=None, temp=None):
        self.status = status
        self.msg = msg
        self.country = country
        self.feels_like = feels_like
        self.temp = temp


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def result_weather_mapper(result) -> ResultWeather:

    result = result.json

    country = result["sys"]["country"]
    feels_like_kelvin = result["main"]["feels_like"]
    temp_kelvin = result["main"]["temp"]

    feels_like_celsius = str((round(int(kelvin_to_celsius(feels_like_kelvin)), 2)))
    temp_celsius = str(round(int(kelvin_to_celsius(temp_kelvin)), 2))

    return ResultWeather(
        status="success",
        country=country,
        feels_like=feels_like_celsius,
        temp=temp_celsius,
    )


@app.route("/")
def home():
    # result = ResultWeather("brasil", "brasil", 25)
    result = ResultWeather(status=None)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
