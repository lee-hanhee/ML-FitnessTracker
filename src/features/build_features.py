import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter, PrincipalComponentAnalysis
from TemporalAbstraction import NumericalAbstraction


# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle("../../data/interim/02_outliers_removed_chauvenets.pkl")  # Load the processed data

predictor_columns = list(df.columns[:6])  # Select the columns to check for outliers

# Plot settings 
plt.style.use("fivethirtyeight")  # Set the style of the plot
plt.rcParams["figure.figsize"] = (20, 5)  # Set the size of the figure
plt.rcParams["figure.dpi"] = 100  # Set the line width of the plot
plt.rcParams["lines.linewidth"] = 2  # Set the line width of the plot

# --------------------------------------------------------------
# Dealing with missing values (imputation)
# --------------------------------------------------------------
for col in predictor_columns:
    df[col] = df[col].interpolate() # Interpolate missing values linearly
    
df.info()

# --------------------------------------------------------------
# Calculating set duration
# --------------------------------------------------------------

duration = df[df["set"] == 1].index[-1] - df[df["set"] == 1].index[0] # Calculate the duration of the first set

duration.seconds # Convert the duration to seconds

for s in df["set"].unique(): # Loop over the unique values of the set column
    
    start = df[df["set"] == s].index[0] # Get the start time of the set
    stop = df[df["set"] == s].index[-1] # Get the stop time of the set
    
    duration = stop - start # Calculate the duration of the set
    df.loc[(df["set"] == s), "duration"] = duration.seconds # Assign the duration to the duration column
    
duration_df = df.groupby(["category"])["duration"].mean() # Calculate the mean duration per category

duration_df.iloc[0] / 5 # Calculate the mean duration of the first category
duration_df.iloc[1] / 10  # Calculate the mean duration of the second category

# --------------------------------------------------------------
# Butterworth lowpass filter
# --------------------------------------------------------------

df_lowpass = df.copy() # Create a copy of the dataframe
LowPass = LowPassFilter() # Create an instance of the LowPassFilter class

fs = 1000 /200 # Set the sampling frequency
cutoff = 1.3

df_lowpass = LowPass.low_pass_filter(df_lowpass, "acc_y", fs, cutoff, order=5) # Apply the lowpass filter to the acc_y column

subset = df_lowpass[df_lowpass["set"] == 45] # Select the 45th set
print(subset["label"][0]) # Print the label of the 45th set

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10)) # Create a figure with two subplots 
ax[0].plot(subset["acc_y"].reset_index(drop=True), label = "raw data") # Plot the raw data
ax[1].plot(subset["acc_y_lowpass"].reset_index(drop=True), label = "butterworth filter") # Plot the lowpass data
ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True) # Add a legend to the first plot
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True) # Add a legend to the second plot


for col in predictor_columns:
    df_lowpass = LowPass.low_pass_filter(df_lowpass, col, fs, cutoff, order=5) # Apply the lowpass filter to the columns
    df_lowpass[col] = df_lowpass[col + "_lowpass"] # Rename the columns
    del df_lowpass[col + "_lowpass"] # Delete the original columns
    
# --------------------------------------------------------------
# Principal component analysis PCA
# --------------------------------------------------------------

df_pca = df_lowpass.copy() # Create a copy of the dataframe
PCA = PrincipalComponentAnalysis() # Create an instance of the PrincipalComponentAnalysis class

pc_values = PCA.determine_pc_explained_variance(df_pca, predictor_columns) # Determine the explained variance of the principal components

# Plot
plt.figure(figsize=(10,10))
plt.plot(range(1,len(predictor_columns) + 1), pc_values)
plt.xlabel("Principal Component Number")
plt.ylabel("Explained Variance")
plt.show()

# Elbow technique: Determine the number of principal components to keep
df_pca = PCA.apply_pca(df_pca, predictor_columns, 3) # Apply PCA to the dataframe

subset = df_pca[df_pca["set"] == 35] # Select the 45th set
subset[["pca_1", "pca_2", "pca_3"]].plot() # Plot the first three principal components

# --------------------------------------------------------------
# Sum of squares attributes
# --------------------------------------------------------------

df_squared = df_pca.copy() # Create a copy of the dataframe

acc_r = df_squared["acc_x"] ** 2 + df_squared["acc_y"] ** 2 + df_squared["acc_z"] ** 2 # Calculate the sum of squares of the acceleration
gyr_r = df_squared["gyr_x"] ** 2 + df_squared["gyr_y"] ** 2 + df_squared["gyr_z"] ** 2 # Calculate the sum of squares of the gyroscope

df_squared["acc_r"] = np.sqrt(acc_r) # Assign the sum of squares of the acceleration to the dataframe
df_squared["gyr_r"] = np.sqrt(gyr_r) # Assign the sum of squares of the gyroscope to the dataframe

subset = df_squared[df_squared["set"] == 14]
subset[["acc_r", "gyr_r"]].plot(subplots=True)

# --------------------------------------------------------------
# Temporal abstraction
# --------------------------------------------------------------



# --------------------------------------------------------------
# Frequency features
# --------------------------------------------------------------


# --------------------------------------------------------------
# Dealing with overlapping windows
# --------------------------------------------------------------


# --------------------------------------------------------------
# Clustering
# --------------------------------------------------------------


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------