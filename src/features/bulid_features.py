import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter , PrincipalComponentAnalysis
from TemporalAbstraction import NumericalAbstraction

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle(r'../../data/interim/02_outliers_removed_chauvenets.pkl')

sensor_col = list(df.columns[:6])


plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 5)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['lines.linewidth'] = 2

# --------------------------------------------------------------
# Dealing with missing values (imputation)
# --------------------------------------------------------------

df.info()
# Interpolation is a technique used in mathematics and statistics to estimate values between two known values. In the context of Pandas DataFrames, interpolation can be applied along rows or columns to estimate missing values based on neighboring data points.
# df['acc_x'].interpolate().isna().sum()

df[df['set']== 30]['acc_x'].plot()

for col in sensor_col:
    df[col] = df[col].interpolate()
    
df.info()

df[df['set']== 30]['acc_x'].plot()

# --------------------------------------------------------------
# Calculating set duration
# --------------------------------------------------------------

#We know that: the heavy set contains 5 repetitions, and medium set contains 10 repetitions for each exercise

#Now we need to know the duration for each set

for set in  df['set'].unique():
    
    strart = df[df['set'] == set].index[0]
    end = df[df['set'] == set].index[-1]
    
    duration = end - strart
    
    df.loc[(df['set'] == set) , 'duration'] = duration.seconds
    

duration_df =  df.groupby('category')['duration'].mean()    

duration_df[0] / 5 # so each repetition take 2.9 sec in heavy set
duration_df[1] / 10 # so each repetition take 2.4 sec in medium set





# --------------------------------------------------------------
# Butterworth lowpass filter
# --------------------------------------------------------------
df_lowpass = df.copy()

LowPass = LowPassFilter()

sampling_frq = 1000 / 200 # # because we are taking the record every 200 ms, so that line calculates number of repetition in 1 sec

cutoff_frq = 1.3 # the low cutoff frequency, meaning more smoothing in signal

LowPass.low_pass_filter(df_lowpass , 'acc_y' , sampling_frq , cutoff_frq)

subset = df_lowpass[df_lowpass["set"] == 45]
print(subset["label"][0])

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
ax[0].plot(subset["acc_y"].reset_index(drop=True), label="raw data")
ax[1].plot(subset["acc_y_lowpass"].reset_index(drop=True), label="butterworth filter")
ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)


for col in sensor_col:
    df_lowpass = LowPass.low_pass_filter(df_lowpass, col, sampling_frq, cutoff_frq, order=5)
    df_lowpass[col] = df_lowpass[col + "_lowpass"]
    del df_lowpass[col + "_lowpass"]

# --------------------------------------------------------------
# Principal component analysis PCA
# --------------------------------------------------------------

df_pca = df_lowpass.copy()
PCA = PrincipalComponentAnalysis()
pc_values =  PCA.determine_pc_explained_variance(df_pca , sensor_col)
plt.plot(range(1, 7) , pc_values)
df_pca = PCA.apply_pca(df_pca , sensor_col , 3 )
subset = df_pca[df_pca["set"] == 35] 

subset[['pca_1' , 'pca_2' , 'pca_3']].plot()

# --------------------------------------------------------------
# Sum of squares attributes
# --------------------------------------------------------------

# To further exploit the data, the scalar magnitudes r of the accelerometer and gyroscope were calculated. 
# r is the scalar magnitude of the three combined data points: x, y, and z. 
# The advantage of using r versus any particular data direction is that it is impartial to device orientation and can handle dynamic re-orientations.
# r is calculated by: r_{magnitude} = sqrt{x^2 + y^2 + z^2}

df_squares = df_pca.copy()

acc_r = df_squares['acc_x'] **2 + df_squares['acc_y'] **2 +df_squares['acc_z'] **2 
gyr_r = df_squares['gyr_x'] **2 + df_squares['gyr_y'] **2 +df_squares['gyr_z'] **2 


df_squares['acc_r'] = np.sqrt(acc_r)
df_squares['gyr_r'] = np.sqrt(gyr_r)


df_squares
subset = df_squares[df_pca["set"] == 18] 

subset[['acc_r' , 'gyr_r' ]].plot(subplots = True)

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