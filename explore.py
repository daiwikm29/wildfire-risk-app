import pandas as pd
import numpy as np
#continuin pattern of tablifying terrain into 0.25
terrain_table = pd.read_parquet("data/raw/terrain/terrain_ca.parquet")
latitudes_terrain = terrain_table["lat"]
longitudes_terrain = terrain_table["lon"]

grid_v = np.floor(latitudes_terrain / 0.25) * 0.25
terrain_table["grid_lat"] = grid_v

grid_v = np.floor(longitudes_terrain / 0.25) * 0.25
terrain_table["grid_lon"] = grid_v

#piles all terrain data that fall in the same 0.25 grid square since some terrain data is more granular than 0.25 degree and we want to make sure we have one row per grid square
terrain_agg_table =terrain_table.groupby(["grid_lat", "grid_lon"]).agg({"elevation": "mean", "slope": "mean", "aspect_sin": "mean", "aspect_cos": "mean"}).reset_index()

#creating master table to add every year to
master_list = []

#making sure that this process actually gets applied to each year, not just 2021
for i in range(2021, 2026):
    #put everyting into a table from start of 2016 season to end of 2016 season
    firms_table = pd.read_parquet(f"data/raw/firms/firms_{i}-05-01_{i}-10-31.parquet")

    #extracts lat and lon from the table
    latitudes_firms = firms_table["latitude"]
    longitudes_firms = firms_table["longitude"]

    #make numbers nice and rounded to the nearest 0.25
    grid_v = np.floor(latitudes_firms / 0.25) * 0.25
    firms_table["grid_lat"] = grid_v

    grid_v = np.floor(longitudes_firms / 0.25) * 0.25
    firms_table["grid_lon"] = grid_v
            
    #print to make sure everyting is working correctly and the lat and lon are rounded 
    print(firms_table[["grid_lat", "grid_lon"]].head())

    #create weather table from start of 2021 season to end of 2021 season
    weather_table = pd.read_parquet(f"data/raw/weather/weather_{i}-05-01_{i}-10-31.parquet")

    #extracts lat and lon from the table same as before
    latitudes_weather = weather_table["lat"]
    longitudes_weather = weather_table["lon"]

    grid_v = np.floor(latitudes_weather / 0.25) * 0.25
    weather_table["grid_lat"] = grid_v

    grid_v = np.floor(longitudes_weather / 0.25) * 0.25
    weather_table["grid_lon"] = grid_v

    #since Firms data include informatoin of the fire detectoin which is informatoin of the fire
    # after its been detected we only need the grid lat and lon to mark the cell and the date to mark the when
    #so we need to extract the unique combinations of grid lat, grid lon, and acq_date to get the unique fire days
    # so that we can merge it the other data to create a label for when the fire occured.
    fire_days_table = firms_table.drop_duplicates(subset=["grid_lat", "grid_lon", "acq_date"])

    #adding a column to the fire_days_table to mark the fire days with a 1
    fire_days_table["label"] = 1

    #renaming the acq_date column to date to match the weather table for merging
    fire_days_table = fire_days_table.rename(columns={"acq_date": "date"})

    #checking progress on all updates essentially
    print(len(firms_table), len(fire_days_table), fire_days_table.head())

    #merge all of the data together to create a final table that has all of the information we need for our model
    final_table = pd.merge(weather_table, terrain_agg_table, on=["grid_lat", "grid_lon"], how="left")
    base_table = pd.merge(final_table, fire_days_table, on=["grid_lat", "grid_lon", "date"], how="left")
    #filling in the missing values in the label column with 0 to indicate no fire on that day
    base_table["label"] = base_table["label"].fillna(0.0)
    print(len(base_table), base_table["label"].value_counts())

    #addressing flag of possible iniculsion of cells that are in ocean and need to be removed from data set
    bad_cells = terrain_agg_table[(terrain_agg_table["elevation"] == 0) & (terrain_agg_table["slope"] == 0)]
    overlap = pd.merge(bad_cells, fire_days_table, on=["grid_lat", "grid_lon"])
    print(len(overlap), overlap.head())

    #removing the bad cells from the base_table to ensure that we only have land cells in our final dataset
    base_table = base_table[~(((base_table["elevation"] == 0) & (base_table["slope"] == 0)))]
    print(len(base_table), base_table["label"].value_counts())

    #removing all unneeded colums from firms
    base_table = base_table.drop(columns=["latitude", "longitude", "confidence", "source", "acq_time", "frp", "daynight"])
    master_list.append(base_table)
    
  
master_table = pd.concat(master_list)
master_table["year"] = master_table["date"].str[:4]  
  
#combinging both weather patches
weather_patch = pd.read_parquet("data/processed/weather_patch.parquet")
weather_patch_2 = pd.read_parquet("data/processed/weather_patch_2.parquet")
combined_weather_patch = pd.concat([weather_patch, weather_patch_2])

#merging the combined weather patch with the master table to fill in any missing data
master_table = pd.merge(master_table, combined_weather_patch, on=["grid_lat", "grid_lon","date"], how="left", suffixes=("", "_patch"))

master_table["relative_humidity_2m_mean"] = master_table["relative_humidity_2m_mean"].fillna(master_table["relative_humidity_2m_mean_patch"])
master_table["wind_speed_10m_max"] = master_table["wind_speed_10m_max"].fillna(master_table["wind_speed_10m_max_patch"])
master_table["wind_gusts_10m_max"] = master_table["wind_gusts_10m_max"].fillna(master_table["wind_gusts_10m_max_patch"])
master_table["precipitation_sum"] = master_table["precipitation_sum"].fillna(master_table["precipitation_sum_patch"])

master_table = master_table.drop(columns=["relative_humidity_2m_mean_patch", "wind_speed_10m_max_patch", "wind_gusts_10m_max_patch", "precipitation_sum_patch"])
master_table = master_table.sort_values(["grid_lat", "grid_lon", "date"])

master_table["precip_7d_sum"] = master_table.groupby(["grid_lat","grid_lon","year"])["precipitation_sum"].transform(lambda x: x.rolling(7).sum())
master_table["precip_30d_sum"] = master_table.groupby(["grid_lat","grid_lon","year"])["precipitation_sum"].transform(lambda x: x.rolling(30).sum())
master_table["temp_7d_mean"] = master_table.groupby(["grid_lat","grid_lon","year"])["temperature_2m_max"].transform(lambda x: x.rolling(7).mean())
master_table["humidity_7d_mean"] = master_table.groupby(["grid_lat","grid_lon","year"])["relative_humidity_2m_mean"].transform(lambda x: x.rolling(7).mean())

print(master_table.duplicated(subset=["grid_lat","grid_lon","date"]).sum())
print(master_table.isna().sum())
master_table.to_parquet("data/processed/training_table.parquet", index=False)

terrain_agg_table.to_parquet("data/processed/terrain_lookup.parquet", index=False)









