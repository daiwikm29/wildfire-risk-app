# SCOPE.md — Wildfire Risk Checker (CAC 2026)

## What it does (MVP)
1. **Primary:** user clicks a point on a Leaflet map → a Flask endpoint returns a
   wildfire risk score for that location (and date, if the model is date-aware).
2. **Stretch (only after #1 works end to end):** an address search box that
   geocodes to lat/lon and calls the same risk endpoint. Runs a script on some hosted server to collect the day's relavant stats in that area to provided a better risk score.

## Deployment
- **Primary target:** run locally, record the demo video from that. This is
  what has to work by Oct 26.
- **Stretch:** deploy to a free host so judges can
  click a live link. Don't start this until the local app is solid and the video
  is recorded

## Architecture
Not decided yet, when I actually reach each phase, not sketched in advance. Each phase
below gets an "Architecture decided" sub-note added here once it's real, with the
reasoning, not just the conclusion.

## Phase checkpoints
Update PROGRESS.md's
status log as each phase completes; that log is the real timeline record.

1. Data exploration — load and find the join key ✅ done
2. Feature engineering — joined table with fire/no-fire labels + weather features
   ✅ done for one season (`data/processed/base_table.parquet`, 2021 only, 227,792 rows).
   **Not done across all five seasons** — see PROGRESS.md Phase 2.5.
3. Model training — baseline model, date-based split, PR-AUC/Brier evaluation
   (**current phase**; blocked on 2.5 first — a date-based split needs more than one season)
4. Flask API — `/api/risk` wired to the trained model
5. Leaflet frontend — map-click UI calling the API, risk shown visually
6. Polish + demo video — **this is the real deadline deliverable**
7. Stretch: address search — geocode → same risk endpoint
8. Stretch: live deploy — only if time remains after #6
9. Stretch: Use Firms to drive Live map as well as prediction, every couple weeks go down for maintenence to retrain model on new FRIMS data.

## Out of scope (unless there's time after #6)
No user accounts, no historical-trends dashboard, no mobile app.
