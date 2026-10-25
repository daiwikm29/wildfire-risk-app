import os
os.environ["OMP_NUM_THREADS"] = "1"
import pandas as pd
from sklearn.metrics import average_precision_score
from sklearn.ensemble import HistGradientBoostingClassifier
import joblib
import json

training_table = pd.read_parquet("data/processed/training_table.parquet")

#creating test table for end of training and training table for model training
test_set = training_table[training_table["year"] == "2025"]
training_set = training_table[training_table["year"] != "2025"]
print(len(test_set), len(training_set), test_set["label"].mean(), training_set["label"].mean())

test_set = pd.merge(test_set, training_set.groupby(["grid_lat", "grid_lon"])["label"].mean().reset_index().rename(columns={"label": "historical_rate"}), on=["grid_lat", "grid_lon"], how="left")
test_set.to_parquet("data/processed/test_set.parquet", index=False)
print(average_precision_score(test_set["label"], test_set["historical_rate"]))

#seperating ttraining set into features and labels
feature_cols = ["temperature_2m_max", "temperature_2m_min", "relative_humidity_2m_mean", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_sum", "elevation", "slope", "aspect_sin", "aspect_cos"]
X_train = training_set[feature_cols]
y_train = training_set["label"].astype(int)

X_test = test_set[feature_cols]
y_test = test_set["label"].astype(int)

model = HistGradientBoostingClassifier(random_state=42)
model.fit(X_train, y_train)
y_prediction = model.predict_proba(X_test)[:, 1]
print(average_precision_score(y_test, y_prediction))
joblib.dump(model, "models/model.joblib")
with open("features.json", "w", encoding="utf-8") as file:
    json.dump(feature_cols, file, indent=4)

results = pd.DataFrame({"predicted": y_prediction, "actual": y_test})
results["bin"] = pd.qcut(results["predicted"], 10, labels=False)
print(results.groupby("bin")[["predicted", "actual"]].mean())

#training weather and terrain separately
terrain_features = ["elevation", "slope", "aspect_sin", "aspect_cos"]
X_train_terrain = training_set[terrain_features]
weather_features = ["temperature_2m_max", "temperature_2m_min", "relative_humidity_2m_mean", "wind_speed_10m_max", "wind_gusts_10m_max", "precipitation_sum", "temp_7d_mean", "humidity_7d_mean"]

X_train_weather = training_set[weather_features]

X_test_terrain = test_set[terrain_features]
X_test_weather = test_set[weather_features]

model_terrain = HistGradientBoostingClassifier(random_state=42)
model_terrain.fit(X_train_terrain, y_train)
print(average_precision_score(y_test, model_terrain.predict_proba(X_test_terrain)[:, 1]))

model_weather = HistGradientBoostingClassifier(random_state=42)
model_weather.fit(X_train_weather, y_train)
print(average_precision_score(y_test, model_weather.predict_proba(X_test_weather)[:, 1]))

rate_table = training_set.groupby(["grid_lat","grid_lon"])["label"].mean().reset_index().rename(columns={"label": "historical_rate"})
rate_table.to_parquet("data/processed/historical_rate_lookup.parquet", index=False) 
training_set = pd.merge(training_set, rate_table, on=["grid_lat","grid_lon"], how="left")

feature_cols_v2 = feature_cols + ["historical_rate"]
X_train2 = training_set[feature_cols_v2]
X_test2 = test_set[feature_cols_v2]

model2 = HistGradientBoostingClassifier(random_state=42)
model2.fit(X_train2, y_train)
print(average_precision_score(y_test, model2.predict_proba(X_test2)[:, 1]))

joblib.dump(model2, "models/model.joblib")
with open("features.json", "w", encoding="utf-8") as file:
    json.dump(feature_cols_v2, file, indent=4)
