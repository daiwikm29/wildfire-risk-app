#using this to call all of the missing data in
import urllib.request
import urllib.error
import time
import json
import ssl
import certifi
import pandas as pd

print(f"certifi version: {certifi.__version__}, bundle path: {certifi.where()}\n")

# force this SSL context to use certifi's CA bundle explicitly, rather than
# relying on OpenSSL's/Windows' own default trust store, which may be stale
ctx = ssl.create_default_context(cafile=certifi.where())

coords = pd.read_parquet("data/processed/remaining_data.parquet")

patches = []
for i,row in enumerate(coords.itertuples()):
    lat = row.grid_lat
    lon = row.grid_lon
    year = row.year
    
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date={year}-05-01&end_date={year}-10-31"
        f"&daily=wind_speed_10m_max,wind_gusts_10m_max,relative_humidity_2m_mean,precipitation_sum"
        f"&timezone=auto"
    )
    try:
        with urllib.request.urlopen(url, timeout=15, context=ctx) as resp:
            status = resp.status
            body = json.loads(resp.read())
            ok = "daily" in body
            if ok:
                weather_data = pd.DataFrame(body["daily"])
                weather_data["grid_lat"] = lat
                weather_data["grid_lon"] = lon
                weather_data = weather_data.rename(columns={"time": "date"})
                patches.append(weather_data)
    except Exception as e:
        ok = False
        print(f"failed: {e}")
    time.sleep(3)
if patches:
    patch_table = pd.concat(patches)
    patch_table.to_parquet("data/processed/weather_patch_2.parquet", index=False)
    print(len(patch_table))
else:
    print("nothing is working you should prob do smth else or your cooked")

