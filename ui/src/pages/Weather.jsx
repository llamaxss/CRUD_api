import React, { useState } from "react";

import { getWetherbyCityName, getWetherbyGeoCode } from "../util/WeatherHttp";

function Weather() {
  const [result, setResult] = useState();
  const [error, setError] = useState(true);

  async function handleSubmit(mode, formData) {
    if (mode === "geolocation") {
      const lat = formData.get("lat");
      const lon = formData.get("lon");
      getWetherbyGeoCode(lat, lon)
        .then((res) => {
          setResult(res);
          setError(false);
        })
        .catch((error) => {
          console.error("Error:", error);
          setError(error.message);
        });
    } else if (mode === "city-name") {
      const cityName = formData.get("cityName");
      await getWetherbyCityName(cityName)
        .then((res) => {
          setResult(res);
          setError(false);
        })
        .catch((error) => {
          console.error("Error:", error);
          setError(error.message);
        });
    }
  }

  return (
    <div>
      <div style={{ display: "flex" }}>
        <form
          id="city-name-form"
          action={(formData) => handleSubmit("city-name", formData)}
        >
          <p>Find with city name</p>
          <input type="text" name="cityName" placeholder="City name" />
          <button type="submit">Submit</button>
        </form>
        <p style={{ margin: "0.5rem" }}></p>
        <form
          id="geolocation-form"
          action={(formData) => handleSubmit("geolocation", formData)}
        >
          <p>Find with lat lon</p>
          <div style={{ width: "10rem", display: "inline" }}>
            <input
              type="text"
              name="lat"
              placeholder="Lat"
              style={{ width: "10em" }}
            />
            <input
              type="text"
              name="lon"
              placeholder="Lon"
              style={{ width: "10em" }}
            />
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
      {!error ? (
        <div>
          <h2>Result</h2>
          <p>Country: {result.country}</p>
          <p>Feels like: {result.feels_like} C&deg;</p>
          <p>Temperature: {result.temp} C&deg;</p>
        </div>
      ) : (
        <div>
          <h2>{error}</h2>
        </div>
      )}
    </div>
  );
}

export default Weather;
