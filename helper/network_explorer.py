import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Helper file to eplore the data

# Plot the distribution of the number of ratings per user
def plot_nb_of_ratings(ratings : pd.DataFrame):
    # Count the nb. of ratings per user
    val_c = ratings['user_id'].value_counts()
    # Remove labels
    a = np.array(list(val_c))
    # Count the nb. of users with X ratings
    vc_c = np.unique(a, return_counts=True)
    # Change figure size
    plt.figure(figsize=(12, 7))
    # Plot histogram
    plt.hist(vc_c[0], bins=200, color='darkolivegreen')
    plt.yscale('log')
    # Add legend
    plt.xlabel("Number of ratings per user")
    plt.ylabel("Amount of users")
    plt.title("Number of users with given ratings")
    # Show plot
    plt.show()
    return vc_c
