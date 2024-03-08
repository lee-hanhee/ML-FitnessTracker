import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle('../../data/interim/01_data_processed.pkl')

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------

#We plotting single set because if we were plotting all sets, the plot wouldn't be useful and would not be clear to interpret
single_set =  df[df['set'] == 2]

# df['set'].unique()

plt.plot(single_set['acc_y'])

plt.plot(single_set['acc_y'].reset_index(drop= True)) #It tells us how many samples were in the set 




# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
# df['label'].unique()

for label in df['label'].unique():
    subset = df[df['label'] == label]
    # display(subset.head(2))
    fig ,ax =plt.subplots()
    plt.plot(subset['acc_y'].reset_index(drop= True) , label=label)
    plt.legend()
    plt.show()
    
for label in df['label'].unique():
    subset = df[df['label'] == label]
    # display(subset.head(2))
    fig ,ax =plt.subplots()
    plt.plot(subset[:100]['acc_y'].reset_index(drop= True) , label=label)
    plt.legend()
    plt.show()
    
# by show those plots, we note that there are different pattern for each exercise, which is good for our ML model

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------

mpl.style.use('seaborn-v0_8-deep')
mpl.rcParams['figure.figsize'] = (20, 5)
mpl.rcParams['figure.dpi'] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------


# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------


# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------


# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------