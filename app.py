import flask
import joblib
import json
import pandas as pd
import ssl
import certifi
import numpy as np
import urllib.request
import functools
import datetime


with open("features.json") as f:
   feature_cols = json.load(f)

app = flask.Flask(__name__)
model = joblib.load("models/model.joblib")
terrain_lookup = pd.read_parquet("data/processed/terrain_lookup.parquet")
historical_rate_lookup = pd.read_parquet("data/processed/historical_rate_lookup.parquet")

tx = ssl.create_default_context(cafile=certifi.where())

@functools.lru_cache(maxsize=256)
def fetch_weather(lat_centre, lon_centre, date_str):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat_centre}&longitude={lon_centre}"
        f"&daily=temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean,"
        f"wind_speed_10m_max,wind_gusts_10m_max,precipitation_sum"
        f"&timezone=auto"
    )
    with urllib.request.urlopen(url, timeout=15, context=tx) as resp:
        body = json.loads(resp.read())
    if "daily" not in body:
        raise Exception("weather fetch failed")
    return body["daily"]


@app.route("/api/risk")
def predict_risk():
    lat = flask.request.args.get("lat", type=float)
    lon = flask.request.args.get("lon", type=float)
    if lat is None or lon is None:
        return flask.jsonify({"error": "lat and lon are required"}), 400
    grid_lat = np.floor(lat / 0.25) * 0.25
    grid_lon = np.floor(lon / 0.25) * 0.25
    match = historical_rate_lookup[ (historical_rate_lookup["grid_lat"] == grid_lat) & (historical_rate_lookup["grid_lon"] == grid_lon)]
    if match.empty:
      return flask.jsonify({"error": "no data for this location"}), 404
    else:
        historical_rate = match["historical_rate"].values[0]
        terrain_match = terrain_lookup[(terrain_lookup["grid_lat"] == grid_lat) & (terrain_lookup["grid_lon"] == grid_lon)]
        elevation = terrain_match["elevation"].values[0]
        slope = terrain_match["slope"].values[0]
    
        today_str = datetime.date.today().isoformat()
    lat_centre = grid_lat + 0.125
    lon_centre = grid_lon + 0.125

    try:
        daily = fetch_weather(lat_centre, lon_centre, today_str)
    except Exception:
        return flask.jsonify({"error": "weather service unavailable"}), 503

    temperature_2m_max = daily["temperature_2m_max"][0]
    temperature_2m_min = daily["temperature_2m_min"][0]
    relative_humidity_2m_mean = daily["relative_humidity_2m_mean"][0]
    wind_speed_10m_max = daily["wind_speed_10m_max"][0]
    wind_gusts_10m_max = daily["wind_gusts_10m_max"][0]
    precipitation_sum = daily["precipitation_sum"][0]
    response_date = daily["time"][0]
    feature_values = {
        "temperature_2m_max": temperature_2m_max,
        "temperature_2m_min": temperature_2m_min,
        "relative_humidity_2m_mean": relative_humidity_2m_mean,
        "wind_speed_10m_max": wind_speed_10m_max,
        "wind_gusts_10m_max": wind_gusts_10m_max,
        "precipitation_sum": precipitation_sum,
        "elevation": elevation,
        "slope": slope,
        "aspect_sin": terrain_match["aspect_sin"].values[0],
        "aspect_cos": terrain_match["aspect_cos"].values[0],
        "historical_rate": historical_rate
    }
    input_df = pd.DataFrame([feature_values])[feature_cols]
    risk = float(model.predict_proba(input_df)[:, 1][0])

    return flask.jsonify({
        "risk": risk,
        "grid_lat": grid_lat,
        "grid_lon": grid_lon,
        "historical_rate": historical_rate,
        "elevation": elevation,
        "slope": slope,
        "aspect_sin": terrain_match["aspect_sin"].values[0],
        "aspect_cos": terrain_match["aspect_cos"].values[0],
        "date": response_date,
        "weather": {
            "temperature_2m_max": temperature_2m_max,
            "temperature_2m_min": temperature_2m_min,
            "relative_humidity_2m_mean": relative_humidity_2m_mean,
            "wind_speed_10m_max": wind_speed_10m_max,
            "wind_gusts_10m_max": wind_gusts_10m_max,
            "precipitation_sum": precipitation_sum
        },
        "units": "metric"
    })

@app.route("/")
def index():
    return app.send_static_file("index.html")

app.run(debug=False)


