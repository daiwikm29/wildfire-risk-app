# AI Usage Disclosure Log — Wildfire Risk Checker (CAC 2026)

Required under 2026 CAC Rules §3/§7.3. One entry per session that involves Claude,
added the same day. Committed — not gitignored — so it's visible on GitHub.

**Template:**
```
## YYYY-MM-DD
- **Worked on:**
- **Claude did:** 
- **I wrote/decided:**

```

---

## 2026-08-08
- **Worked on:** Project setup - setting up rules for claude and ai usage - created various meta docs (this file, CLAUDE.md, SCOPE.md, PROGRESS.md, .gitignore, requirements.txt).
- **Claude did:** Wrote these meta-docs directly — explicitly permitted under CLAUDE.md's "MAY do" list since they aren't the app itself. Asked clarifying questions about MVP scope, deployment priority, milestone pacing, and this log's format before drafting SCOPE.md/PROGRESS.md/ai_usage_log.md content that wasn't otherwise available in this session.
- **I wrote/decided:** User interface scope (interactive map in which risk is then displayed), deployment priority (local demo video first, live hosting only if time remains), and this log's format (structured template). No application code exists yet.


## 2026-08-08 
- **Worked on:**  going through raw weather and firms data and doing various comparison suchs as checking rows and comparing long and lats covered by each (slight gaps on edged, however they are very small)
- **Claude did:** debugged logic and suggested some tools to use in pandas library
- **I wrote/decided:** all comparison and combining logic and code. Also decided what to compare.


## 2026-08-08
- **Worked on:** Investigated additional data sources like ERA5 and gridmet for additional info
- **Claude did:** Helped bring in data from various sources overnight
- **I wrote/decided:** Asked for the performance-vs-time-cost research instead of accepting a recommendation. Decided to keep terrain available as an option rather than committing to it now — whether it actually goes in the model is a Phase 2 decision I'll make with the tradeoff in front of me.


## 2026-08-08
- **Worked on:** Pinning down exactly how much data I actually need and thinking through whether the app should show a static terrain-based risk map or something driven by current weather.
- **Claude did:** Checked the actual row counts of theather files and found 9 of 10 were empty 0-row stubs — the 0.1° ingestion had never finished. Traced down the only complete Open-Meteo dataset (the 0.25° archive, 5 seasons) and swapped it in, then wrote
  the corrected data inventory into PROGRESS.md
- **I wrote/decided:** After finally shortlisting different possible data sets finally selected weather, data from Firms, and terrian in order to train model

## 2026-08-011 --> 2026-08-12 
- **Worked on:** Combing data together and essentialy converting it into a way to be used to train the model, this includes all of the micro steps involved such as trimming away the firms data on detected fire.
- **Claude did:** flagged certain bugs and sytax errors and gave already imported function recogmendations from imported librarys
- **I wrote/decided:** all the code in explore.py as well as the comments

## 2026-09-01 --> 2026-09-9 
**Worked on:** Getting all of the missing data idenitifed and over the course of a couple days attempting to get all of the missing and data and combining them to the traning data
- **Claude did:** flagged certain bugs and sytax errors and gave already imported function recogmendations from imported librarys like last time
- **I wrote/decided:** all the code in explore.py as well as pipeline.py adjusting the code inside to only get what we need.

## 2026-09-09 --> 2026-09-14 
**Worked on:** Merged both weather patches into traning and checked for gaps. Built train.py which a 2021-2024 train and 2025 teset. Split featuers into terrain only and weather only to see where signal comes from. Added historical rate. Tested other pfeatures but ended up making model worse. Saved the model. Trimmed unnecassary code.
- **Claude did:** Reviewed and debugged code, pointed out bugs such as unassigned results, .drop() used where I meant to select columns, a wrong import path, a duplicate merge, and a leaky lookup table. Explained the fixes before I made them. Explained concepts: PR-AUC, X/y, predict_proba, calibration, rolling windows, and why terrain drives ranking across cells while weather still moves one cell's score. Ran read-only checks on the data (row counts, missing values, grid alignment). Checked that the Open-Meteo forecast API returns the same variables. Wrote no .py code.
- **I wrote/decided:** all the code in explore.py, train.py, pipeline.py, and kept model2. Deleted all dead code.

## 2026-10-06 --> 2026-10-13 
**Worked on:** Finished setting up api for model and creating cache for the maine app backend.
- **Claude did:** Explained concpets using in app.py and reviewed my code at each step, catching misplaced code after app.run, a missing return, a nonexistent terrain column, and premature model calls. Ran read-only checks, and syntax checks
- **I wrote/decided:** Typed all of thge code in app.py

## 2026-10-18 --> 2026-10-21 
**Worked on:** The basic frontend (map, sidebar, risk label, weather display), the / route, public hosting through a Cloudflare tunnel, and finding that Nevada/Arizona cells return predictions.
- **Claude did:** Explained HTML, CSS, and JavaScript concepts (tags, ids, selectors, flexbox, fetch/async/await, response.ok, template strings, event listeners).
Gave Leaflet facts: the CDN links, the OpenStreetMap tile URL, L.map / setView / tileLayer, and that right-click is the 'contextmenu' event.
Reviewed my HTML and JS and pointed out bugs: wrong API path, a typo, missing error branch, quoted variable, missing # on colors, wrong weather names, the #body selector, code outside the script/style tags.
- **I wrote/decided:** The layout and all of hte code in index.html, and found the Nevada bug while testing.

