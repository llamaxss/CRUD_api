from flask import (
    request,
    Blueprint,
)

from src.weather_api.util import handle_weather_geocode, handle_weather_city

weather_api_bp = Blueprint("weather_api_bp", __name__, url_prefix="/api/weather")


@weather_api_bp.route("/city", methods=["GET"])
def fetch_weather_by_city():
    city_name = request.args.get("cityName")
    return handle_weather_city(city_name)


@weather_api_bp.route("/geocode", methods=["GET"])
def fetch_weather_by_coordinates():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    return handle_weather_geocode(lat, lon)


if __name__ == "__main__":
    weather_api_bp.run(debug=True)
