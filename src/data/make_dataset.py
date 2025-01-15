import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------

single_file_acc = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv") # Read a single accelerometer file

single_file_gyr = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv") # Read a single gyroscope file

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------

files = glob("../../data/raw/MetaMotion/*.csv") # List all files in the directory
len(files) # Check how many files we have

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------

data_path = "../../data/raw/MetaMotion/" # Define the path to the data
f = files[0] # Get the first file

participant = f.split("-")[0].replace(data_path, "") # Get the participant ID, e.g. A
label = f.split("-")[1] # Get the activity label, e.g. bench
category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019") # Get the category, heavy or light

df = pd.read_csv(f) # Read the file. 

df["participant"] = participant # Add the participant ID to the dataframe
df["label"] = label # Add the activity label to the dataframe
df["category"] = category # Add the category to the dataframe

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------

acc_df = pd.DataFrame() # Create an empty dataframe
gyr_df = pd.DataFrame() # Create an empty dataframe

# Set number is an identifier for the accelerometer and gyroscope data
acc_set = 1 # Set the accelerometer set
gyr_set = 1 # Set the gyroscope set

for f in files: # Loop through all files
   
    participant = f.split("-")[0].replace(data_path, "") # Get the participant ID, e.g. A
    label = f.split("-")[1] # Get the activity label, e.g. bench
    category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019") # Get the category, heavy or light
    
    df = pd.read_csv(f) # Read the file.
    
    df["participant"] = participant # Add the participant ID to the dataframe
    df["label"] = label # Add the activity label to the dataframe
    df["category"] = category # Add the category to the dataframe
    
    # Go to the accelerator or gyroscope set
    if "Accelerometer" in f:
        df["set"] = acc_set # Add the set number to the dataframe
        acc_set += 1 # Increment the set number
        acc_df = pd.concat([acc_df, df]) # Concatenate the dataframe.
    
    if "Gyroscope" in f:
        df["set"] = gyr_set
        gyr_set += 1
        gyr_df = pd.concat([gyr_df, df]) # Concatenate the dataframe.

# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------

acc_df.info()

pd.to_datetime(df["epoch (ms)"], unit="ms") # Convert the epoch to datetime

acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms") # Set the index to the datetime
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms") # Set the index to the datetime

del acc_df["epoch (ms)"] # Delete the epoch column
del acc_df["time (01:00)"] # Delete the time column
del acc_df["elapsed (s)"] # Delete the elapsed column

del gyr_df["epoch (ms)"] 
del gyr_df["time (01:00)"]
del gyr_df["elapsed (s)"]

# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------

files = glob("../../data/raw/MetaMotion/*.csv")  # List all files in the directory
data_path = "../../data/raw/MetaMotion/" # Define the path to the data

def read_data_from_files(files):   
    # --------------------------------------------------------------
    # Read all files
    # --------------------------------------------------------------
    
    acc_df = pd.DataFrame() # Create an empty dataframe
    gyr_df = pd.DataFrame() # Create an empty dataframe

    # Set number is an identifier for the accelerometer and gyroscope data
    acc_set = 1 # Set the accelerometer set
    gyr_set = 1 # Set the gyroscope set

    for f in files: # Loop through all files
    
        participant = f.split("-")[0].replace(data_path, "") # Get the participant ID, e.g. A
        label = f.split("-")[1] # Get the activity label, e.g. bench
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019") # Get the category, heavy or light
        
        df = pd.read_csv(f) # Read the file.
        
        df["participant"] = participant # Add the participant ID to the dataframe
        df["label"] = label # Add the activity label to the dataframe
        df["category"] = category # Add the category to the dataframe
        
        # Go to the accelerator or gyroscope set
        if "Accelerometer" in f:
            df["set"] = acc_set # Add the set number to the dataframe
            acc_set += 1 # Increment the set number
            acc_df = pd.concat([acc_df, df]) # Concatenate the dataframe.
        
        if "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df]) # Concatenate the dataframe.
            
    # --------------------------------------------------------------
    # Working with datetimes
    # --------------------------------------------------------------
            
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms") # Set the index to the datetime
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms") # Set the index to the datetime

    del acc_df["epoch (ms)"] # Delete the epoch column
    del acc_df["time (01:00)"] # Delete the time column
    del acc_df["elapsed (s)"] # Delete the elapsed column

    del gyr_df["epoch (ms)"] 
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]
    
    return acc_df, gyr_df

acc_df, gyr_df = read_data_from_files(files)

# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------

data_merged = pd.concat([acc_df.iloc[:,:3], gyr_df], axis=1) # Merge the accelerometer and gyroscope data (column wise)

# Rename columns 
data_merged.columns = [
    "acc_x", 
    "acc_y", 
    "acc_z", 
    "gyr_x",
    "gyr_y", 
    "gyr_z", 
    "participant", 
    "label",
    "category", 
    "set",
]

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz

sampling = {
    "acc_x": "mean", 
    "acc_y": "mean", 
    "acc_y": "mean", 
    "acc_z": "mean", 
    "gyr_x": "mean", 
    "gyr_y": "mean", 
    "gyr_z": "mean", 
    "participant": "last",
    "label": "last",
    "category": "last",
    "set": "last",
}

data_merged[:1000].resample(rule="200ms").apply(sampling)

# Split by day 
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]
data_resampled = pd.concat([df.resample(rule="200ms").apply(sampling).dropna() for df in days])
data_resampled["set"] = data_resampled["set"].astype(int) # Convert the set to integer
data_resampled.info()

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle("../../data/interim/01_data_processed.pkl") # Save the dataset as a pickle file 