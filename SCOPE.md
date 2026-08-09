# SCOPE.md — Wildfire Risk Checker (CAC 2026)

## What it does (MVP)
1. **Primary:** user clicks a point on a Leaflet map → a Flask endpoint returns a
   wildfire risk score for that location (and date, if the model is date-aware).
2. **Stretch (only after #1 works end to end):** an address search box that
   geocodes to lat/lon and calls the same risk endpoint.

## Deployment
- **Primary target:** run Flask locally, record the demo video from that. This is
  what has to work by Oct 26.
- **Stretch:** deploy to a free host (Render/Railway/PythonAnywhere) so judges can
  click a live link. Don't start this until the local app is solid and the video
  is recorded — it's not worth risking the core deliverable.

## Architecture (adjust as it firms up — this is a living doc)
- `data/raw/firms/`, `data/raw/weather/` — existing raw data (carried over, use directly)
- `explore.py` — first step: load one FIRMS parquet + one weather parquet, find the join key
- feature pipeline — TBD once join key is found; produces `training_table.csv` (gitignored)
- model — scikit-learn, algorithm TBD (start simple: logistic regression or random
  forest baseline); evaluate with date-based train/test split, PR-AUC/Brier score
- `app.py` (Flask):
  - `GET /` — serves the Leaflet map page
  - `GET/POST /api/risk` — takes lat/lon (+ optional address for the stretch goal),
    returns a risk score
- `templates/` / `static/` — HTML/JS/Leaflet frontend
- model artifact — saved `.pkl`/`.joblib` (gitignored), loaded by Flask at startup

## Phase checkpoints
No fixed week numbers — budget is 6-10 variable hrs/week. Update PROGRESS.md's
status log as each phase completes; that log is the real timeline record.

1. Data exploration — load FIRMS + weather, find the join key (**current phase**)
2. Feature engineering — joined `training_table.csv` with fire/no-fire labels + weather features
3. Model training — baseline model, date-based split, PR-AUC/Brier evaluation
4. Flask API — `/api/risk` wired to the trained model
5. Leaflet frontend — map-click UI calling the API, risk shown visually
6. Polish + demo video — **this is the real deadline deliverable**
7. Stretch: address search — geocode → same risk endpoint
8. Stretch: live deploy — only if time remains after #6

## Out of scope (unless there's time after #6)
No user accounts, no historical-trends dashboard, no mobile app.
