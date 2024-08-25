import pandas as pd
from glob import glob
import os
import re

def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for f in files:
        normalized_path = os.path.normpath(f)
        filename = os.path.basename(normalized_path)
        participant = filename.split('-')[0]
        label = filename.split('-')[1]
        category_with_digits = filename.split('-')[2].split('_')[0]
        category = re.sub(r'\d+$', '', category_with_digits)
        
        df = pd.read_csv(f)
        df["participant"] = participant
        df["label"] = label
        df["category"] = category
        
        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df], ignore_index=True)
        
        elif "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df], ignore_index=True)
            
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]
    
    return acc_df, gyr_df

files = glob("../../data/raw/MetaMotion/*.csv")

acc_df, gyr_df = read_data_from_files(files)

# Merge Data Frames
final_dataset = pd.concat([acc_df.iloc[:,:3], gyr_df], axis=1)

# Rename Columns
final_dataset.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "label",
    "category",
    "participant",
    "set"
]

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz

sampling =  {
    'acc_x': "mean",
    'acc_y': "mean",
    'acc_z': "mean",
    'gyr_x': "mean",
    'gyr_y': "mean",
    'gyr_z': "mean",
    'label': "last",
    'category': "last",
    'participant': "last",
    'set': "last"
}

final_dataset[:1000].resample(rule="200ms").apply(sampling)

# Split by day
days = [g for n, g in final_dataset.groupby(pd.Grouper(freq = "D"))]

data_resampled = pd.concat([df.resample(rule="200ms").apply(sampling).dropna() for df in days])

data_resampled.info()

data_resampled["set"] = data_resampled["set"].astype("int")

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")