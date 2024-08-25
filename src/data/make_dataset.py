import pandas as pd
from glob import glob
import os

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------

single_file_acc = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")


single_file_gyr = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------

files = glob("../../data/raw/MetaMotion/*.csv")
len(files)

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------

def extract_features(file_path):
    normalized_path = os.path.normpath(file_path)  
    filename = os.path.basename(normalized_path)   
    participant = filename.split('-')[0]           
    label = filename.split('-')[1]                 
    category = filename.split('-')[2].rstrip("123")
    return participant, label, category

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------

acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

acc_set = 1
gyr_set = 1

for f in files:
    participant, label, category = extract_features(f)
    
    df = pd.read_csv(f)
    df["participant"] = participant
    df["label"] = label
    df["category"] = category
    
    if "Accelerometer" in f:
        acc_df = pd.concat([acc_df, df], ignore_index=True)
    
    elif "Gyroscope" in f:
        gyr_df = pd.concat([gyr_df, df], ignore_index=True)
    


# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
