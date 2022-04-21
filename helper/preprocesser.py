import pandas as pd


# Helper file to preprocess the data



# Preprocess the ratings dataframe
#   - Remove users with less than N ratings
#   - TODO Remove outliers users
def preprocess_ratings(ratings : pd.DataFrame, lists : pd.DataFrame, min_ratings : int) -> (pd.DataFrame, pd.DataFrame):
    # Get the users to keep
    users_to_keep = more_than_N_ratings(ratings, min_ratings - 1)
    # Keep only ratings of useful users
    ratings_filtered = ratings[ratings['user_id'].isin(users_to_keep)]
    # Keep only lists of useful users
    lists_filtered = lists[lists['user_id'].isin(users_to_keep)]
    # Return new DataFrames
    return ratings_filtered, lists_filtered


# Get the users that rated at least n-1 movies
def more_than_N_ratings(ratings : pd.DataFrame, n : int) -> list:
    # Get the users with more than n ratings
    has_more = ratings.groupby('user_id')['user_id'].count() > n
    # Select the users to keep
    users_to_keep = has_more[has_more].index
    # Return list of users to keep
    return users_to_keep
