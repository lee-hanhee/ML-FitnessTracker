import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter, PrincipalComponentAnalysis
from DataTransformation import LowPassFilter
from TemporalAbstraction import NumericalAbstraction


# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle('../../data/interim/02_outliers_removed_chauvenets.pkl')

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

cutoff_frq = 1 # the low cutoff frequency, meaning more smoothing in signal

LowPass.low_pass_filter(df_lowpass , 'acc_y' , sampling_frq , cutoff_frq)




# --------------------------------------------------------------
# Principal component analysis PCA
# --------------------------------------------------------------


# --------------------------------------------------------------
# Sum of squares attributes
# --------------------------------------------------------------


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