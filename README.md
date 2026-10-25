# Wildfire Risk Checker

A web app that shows **today's wildfire risk for any spot in California**. Pick a location on the map (right-click) or type a latitude and longitude, and the app returns a risk percentage, a Low / Moderate / High label, and today's weather for that spot.

Built for the 2026 Congressional App Challenge.

## What you see

| Risk | Meaning |
|------|---------|
| **Low** | under 10% |
| **Moderate** | 10% to 30% |
| **High** | over 30% |

The percentage is the model's estimated probability that a fire is detected in that area today. The cutoffs were chosen by looking at how the model's scores lined up with real fires in a held-out year (2025).

## Run it

```
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser. Right-click the map to look up a spot. Left-click and drag to move the map.

The trained model (`models/model.joblib`) and the data are included in this repo, so nothing else needs to be downloaded. Today's weather comes live from the free Open-Meteo forecast API, so you need an internet connection.

## How it works

1. **A grid.** California is split into squares 0.25 degrees wide (about 25 km). Any location is snapped to its square by rounding down to the nearest 0.25. Every dataset and the live app use this same rule, which is what lets them be joined.
2. **Training data** (fire seasons, May to October, 2021 to 2025):
   - **Fire detections** from NASA FIRMS satellites: was a fire detected in this square on this day? (yes or no)
   - **Daily weather** from Open-Meteo: max and min temperature, humidity, wind speed, wind gusts, rainfall.
   - **Terrain**: elevation, slope, and which way the slope faces.
3. **The model.** A gradient-boosting classifier (scikit-learn `HistGradientBoostingClassifier`) trained on 2021 to 2024 and tested on 2025, a year it never saw. Its 11 inputs are the 6 weather values, 4 terrain values, and each square's historical fire rate (how often it burned in the training years). It is scored with PR-AUC, which suits rare events like fires.
4. **The app.** When you pick a spot, the Flask backend snaps it to its square, looks up the terrain and historical rate, fetches today's forecast for the square's center, runs the model, and sends the result to the page. Forecasts are cached so repeat lookups are instant.

## Project layout

| File | Role |
|------|------|
| `pipeline.py` | Re-downloads weather values that were missing from the first download |
| `explore.py` | Snaps everything to the grid, builds the fire/no-fire labels, and merges weather, terrain and fires into the training table |
| `train.py` | Splits train and test by year, trains the model, saves it with its feature list |
| `app.py` | Flask server: the `/api/risk` endpoint and the web page |
| `static/index.html` | The page: Leaflet map, sidebar, and the JavaScript that calls the API |
| `features.json` | The model's 11 input names, in the order it expects |
| `models/` | The trained model |
| `data/` | Raw and processed data used for training and for the app's lookups |

To rebuild from scratch: run `explore.py`, then `train.py`.

## Limitations

- **Coarse squares.** Every point inside a 25 km square gets the same answer, and the score can jump when you cross a square's edge.
- **Not just California.** The grid is a rectangle around the state, so some Nevada and Arizona squares also return predictions.
- **Satellite detections are not confirmed wildfires.** Things like industrial flares can show up as fire detections.
- **Fire season only.** The model was trained on May to October data.
- **A probability, not a guarantee.** It reflects how often similar days and places had fires, and it does not predict where a specific fire will start.

## Tech

Python, pandas, scikit-learn, Flask, HTML, CSS, JavaScript, Leaflet and OpenStreetMap, Open-Meteo, NASA FIRMS.

## AI use

AI use on this project is documented in [ai_usage_log.md](ai_usage_log.md).
