import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pandas.plotting import scatter_matrix
from sklearn import preprocessing
from glob import glob
import matplotlib as mpl
import math

df = pd.read_csv("C:/Users/21294596/OneDrive - Curtin/Coding/Dataset_MC_10k.csv")

print(df.info())
print(df.describe())
num_columns = len(df.columns)

mpl.rcParams.update({'font.size': 10})
mpl.rc('xtick', labelsize=10) 
mpl.rc('ytick', labelsize=10) 
mpl.rc('axes', labelsize=10)

# Calculate the number of rows needed for a 3x5 layout
num_rows = math.ceil(num_columns / 5)

# Set the layout to 3x5
layout = (num_rows, 5)

# Plot histograms
fig, axes = plt.subplots(nrows=num_rows, ncols=5, figsize=(16, 10))

for i, column in enumerate(df.columns):
    ax = axes.flatten()[i]
    ax.hist(df[column], bins=80, alpha=0.7)  # Adjust the number of bins as needed
    ax.set_title(column)
    ax.set_xscale('log')  # Set x-axis to log scale
    
# Hide empty subplots
for i in range(num_columns, num_rows * 5):
    axes.flatten()[i].axis('off')

plt.tight_layout()

# Show the plot
plt.show()
