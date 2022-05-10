import pandas as pd
from faker import Faker
import random
from scipy.sparse import csr_matrix
from tqdm import tqdm

# Helper file to preprocess the data



# Preprocess the ratings dataframe
# First remove movies with less than N1 ratings, then remove users that rated less than N2 movies
# As consequences, there will be movies with less that N1 ratings after removing user
def preprocess_ratings(ratings : pd.DataFrame, lists : pd.DataFrame, min_ratings_user : int=1, min_ratings_movie : int=1) -> (pd.DataFrame, pd.DataFrame):
    # Get the users to keep
    movies_to_keep = more_than_N_ratings_movie(ratings, min_ratings_movie - 1)
    # Keep only ratings of useful users
    ratings_filtered_m = ratings[ratings['movie_id'].isin(movies_to_keep)]
    # Get the users to keep
    users_to_keep = more_than_N_ratings_user(ratings_filtered_m, min_ratings_user - 1)
    # Keep only ratings of useful users
    ratings_filtered = ratings_filtered_m[ratings_filtered_m['user_id'].isin(users_to_keep)]
    # Keep only lists of useful users
    lists_filtered = lists[lists['user_id'].isin(users_to_keep)]
    # Return new DataFrames
    return ratings_filtered, lists_filtered


# Get the users that rated at least n-1 movies
def more_than_N_ratings_user(ratings : pd.DataFrame, n : int) -> list:
    # Get the users with more than n ratings
    has_more = ratings.groupby('user_id')['user_id'].count() > n
    # Select the users to keep
    users_to_keep = has_more[has_more].index
    # Return list of users to keep
    return users_to_keep

# Get the movies that have at least n-1 ratings
def more_than_N_ratings_movie(ratings : pd.DataFrame, n : int) -> list:
    # Get the users with more than n ratings
    has_more = ratings.groupby('movie_id')['movie_id'].count() > n
    # Select the users to keep
    movies_to_keep = has_more[has_more].index
    # Return list of users to keep
    return movies_to_keep


# Create a (random) name for each user id
def create_fake_identities(ids : list):
    # Object to generate fake elements
    fake = Faker()
    # Generate dictionary matching ids to (fake) names
    
    # Vincent: I'm inversing this because I think it makes more sense as the input will be a name -> get id, not the opposite, 
    # which is not practical with dic

    #dir = {id: fake.name() for id in ids}
    dir = {fake.name() : id for id in ids}

    #Add three name that we can always ask
    dir["Carrel Vincent"] = dir.pop(list(dir.keys())[1])
    dir["Corpataux Marine"] = dir.pop(list(dir.keys())[2])
    dir["Fontana Jonas"] = dir.pop(list(dir.keys())[3])

    # Return the new dictionary
    return dir


# Remove x% of the values from the sparse matrix and store them in a dictionary
def prepare_test_data_sparse(user_item_matrix : csr_matrix, test_rate : float) -> (csr_matrix, dict):
    # Create a copy
    matrix = user_item_matrix.copy()
    # Get the number of ratings
    nb_ratings = len(user_item_matrix.nonzero()[0])
    # Sanity check
    assert test_rate >= 0, 'Test rate should be >= 0!'
    assert test_rate < 1, 'Test rate should be < 1!'
    # Get the number of ratings to remove
    nb_to_remove = int(nb_ratings * test_rate)
    # Get random indices to remove
    to_remove = random.sample(range(nb_ratings), nb_to_remove)
    # Get indices of elements
    indices = user_item_matrix.nonzero()
    # Store values
    orig_vals = {}
    # TODO test efficiency and possibly find a more efficient way
    for i in tqdm(to_remove):
        orig_vals[(indices[0][i], indices[1][i])] = matrix[indices[0][i], indices[1][i]]
        matrix[indices[0][i], indices[1][i]] = 0
    # Remove zero values from matrix
    matrix.eliminate_zeros()
    return matrix, orig_vals

# Remove x% of the values from the DataFrame and store them in a dictionary
def prepare_test_data_dense(user_item_matrix : pd.DataFrame, test_rate : float) -> (pd.DataFrame, dict):
    # Create a copy
    matrix = user_item_matrix.copy()
    # Get the number of ratings
    nb_ratings = sum(user_item_matrix.count())
    # Sanity check
    assert test_rate >= 0, 'Test rate should be >= 0!'
    assert test_rate < 1, 'Test rate should be < 1!'
    # Get the number of ratings to remove
    nb_to_remove = int(nb_ratings * test_rate)
    # Get random indices to remove
    to_remove = random.sample(range(nb_ratings), nb_to_remove)
    # Create temp matrix, with 0s instead of NaN
    temp_u_i_m = matrix.fillna(0)
    # Cast to sparse matrix, to get indices of elements
    sparse_m = csr_matrix(temp_u_i_m.values)
    # Remove NaN (now 0)
    sparse_m.eliminate_zeros()
    # Get indices of elements
    indices = sparse_m.nonzero()
    # Store values
    orig_vals = {}
    # TODO test efficiency and possibly find a more efficient way
    for i in tqdm(to_remove):
        orig_vals[(indices[0][i], indices[1][i])] = matrix.iloc[indices[0][i], indices[1][i]]
        matrix.iloc[indices[0][i], indices[1][i]] = None
    # Return df (useless since inplace) and dict
    return matrix, orig_vals
