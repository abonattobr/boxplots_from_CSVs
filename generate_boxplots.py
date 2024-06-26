import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import re
import os
import sys

sns.color_palette("pastel")

# Configurando matplotlib para usar LaTeX globalmente
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{siunitx}",
    "axes.linewidth": 0.25,
    "axes.edgecolor": (0.35,0.35,0.35),
    "axes.labelcolor": (0.35,0.35,0.35),
    "xtick.major.size": 1.5,
    "xtick.major.width": 0.25,
    "xtick.minor.size": 0.75,
    "xtick.minor.width": 0.25,
    "ytick.major.size": 1.5,
    "ytick.major.width": 0.25,
    "ytick.minor.size": 0.75,
    "ytick.minor.width": 0.25,
    "text.color": (0.35,0.35,0.35),
    "xtick.color": (0.35,0.35,0.35),
    "ytick.color": (0.35,0.35,0.35)
})

# Load the CSV files
caso1_df = pd.read_csv('completo_caso1.csv')
caso2_df = pd.read_csv('completo_caso2.csv')
caso3_df = pd.read_csv('completo_caso3.csv')

# Variables to be plotted
var_names = ['Fobj', 'wpw', 'R1', 'L1']

# Create a new figure with 4 subplots (1 row, 4 columns)
fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(7.2, 1.08))

# Define flierprops for the outliers
flierprops = dict(marker='D', markerfacecolor='black', markersize=5)

# Plot the data for each variable, using only the last 40 iterations
for ax, var in zip(axes, var_names):
    if var == 'wpw':
        data1 = caso1_df['wpw'].tail(40)
        data2 = caso2_df['wp1w'].tail(40)
        data3 = caso3_df['wp1w'].tail(40)
    else:
        # Extract data for the current variable from each case
        data1 = caso1_df[var].tail(40)
        data2 = caso2_df[var].tail(40)
        data3 = caso3_df[var].tail(40)
    
    # Create boxplots for each case
    box1 = ax.boxplot(data1, positions=[1], patch_artist=True, 
               boxprops=dict(facecolor="C3", alpha=0.5),
               whiskerprops=dict(color="red"),
               capprops=dict(color="red"),
               medianprops=dict(color="red"),
               flierprops=flierprops)
    
    box2 = ax.boxplot(data2, positions=[2], patch_artist=True, 
               boxprops=dict(facecolor="C0", alpha=0.5),
               whiskerprops=dict(color="black", lw=0.25),
               capprops=dict(color="black", lw=0.25),
               medianprops=dict(color="black", lw=0.25),
               flierprops=flierprops)
    
    box3 = ax.boxplot(data3, positions=[3], patch_artist=True, 
               boxprops=dict(facecolor="C2", alpha=0.5),
               whiskerprops=dict(color="black", lw=0.25),
               capprops=dict(color="black", lw=0.25),
               medianprops=dict(color="black", lw=0.25),
               flierprops=flierprops)
    
    # Set title and labels
    ax.set_title(var)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['C1', 'C2', 'C3'])

    # ax.legend([], [], [], frameon=False)

    plt.subplots_adjust(wspace=0.7, hspace=0.6, left=0.0675, right=0.95, top=0.8, bottom=0.15)

# Add a legend
# handles = [box1["boxes"][0], box2["boxes"][0], box3["boxes"][0]]
# fig.legend(handles, ['C1', 'C2', 'C3'], loc='upper right')

# Save the figure
plt.savefig('completo_modificado_boxplots_ultimas40.pdf')
plt.show()
