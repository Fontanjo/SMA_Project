import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Helper file to eplore the data

# Plot the distribution of the number of ratings per user
def plot_nb_of_ratings(ratings : pd.DataFrame, max_val=None):
    # Count the nb. of ratings per user
    val_c = ratings['user_id'].value_counts()
    # Remove labels
    a = np.array(list(val_c))
    # Count the nb. of users with X ratings
    vc_c = np.unique(a, return_counts=True)
    # Change figure size
    plt.figure(figsize=(12, 7))
    # Reduce array if necessary (to remove big values and make chart more readable)
    if max_val != None:
        v0 = [x for x in vc_c[0] if x < max_val]
        v1 = vc_c[1][:len(v0)]
        vc_c = (v0, v1)
    plt.plot(vc_c[0], vc_c[1])
    plt.yscale('log')
    # Add legend
    plt.xlabel("Number of ratings per user")
    plt.ylabel("Amount of users")
    plt.title("Number of users with given ratings")
    # Show plot
    plt.show()
    return vc_c
    # # Number of bars
    # nbins = 500
    # to_keep = int(fract * len(vc_c[0]))
    # vc_c = (vc_c[0][:to_keep], vc_c[1][:to_keep])
    # len_bins = max(vc_c[0]) / nbins
    # print(len_bins)
    # Get density function
    # density = stats.gaussian_kde(vc_c[0])
    # Plot hist
    # _, x, _ = plt.hist(vc_c[0], bins=nbins,
    # density=False)
    # plt.plot(x, density(x) * sum(vc_c[0]) / len_bins)
    # Plot histogram
    # plt.hist(vc_c[0], bins=200, color='darkolivegreen')
