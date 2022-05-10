###################################################################################################
#
#   User-user collaborative filtering, with the recommendation constrained by social context
#
###################################################################################################



from xmlrpc.client import boolean
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from tqdm import tqdm


#####################################
# Correlation betweens users
#####################################

# Convert the ratings data into a sparse matrix
def ratings_to_sparse(ratings : pd.DataFrame) -> csr_matrix :
    matrix = csr_matrix((ratings["rating_score"],(ratings["user_id"],ratings["movie_id"])))
    return matrix


# Get all the rows and columns not full of 0
# equivalent to the users and movies id
def get_user_movie_id(matrix : csr_matrix) -> (np.array,np.array):
    
    nonzero_row_indice, nonzeros_column_indice = matrix.nonzero()
    user_id = np.unique(nonzero_row_indice)
    movie_id = np.unique(nonzeros_column_indice)

    return user_id,movie_id


# Keep only the sparse matrix with non-zero row and columns
def remove_zero_users_movies(matrix : csr_matrix,user_id : np.array, movie_id : np.array) -> csr_matrix:
    pruned_matrix = matrix[user_id][:,movie_id]
    return pruned_matrix


def compute_average_ratings(user_item_matrix : pd.DataFrame) -> pd.Series:

    return user_item_matrix.mean(skipna=True,axis=1)

# Not ideal because I can't have names in my sparse column/index afaik
# So we must maintain the sparse matrix and two arrays containing the user id and movie id separately 
def get_sparse_user_item(ratings : pd.DataFrame) -> (csr_matrix,np.array,np.array):

    matrix = ratings_to_sparse(ratings)

    user_id,movie_id = get_user_movie_id(matrix)

    user_item = remove_zero_users_movies(matrix,user_id,movie_id)

    return user_item,user_id,movie_id

# Same as above, but return the dense matrix (in a DataFrame)
# Rows: user id
# Columns: movies id
# Takes more time than the sparse one, but easier to add/modify ratings
def get_dense_user_item(ratings : pd.DataFrame) -> pd.DataFrame:

    matrix,user_id,movie_id = get_sparse_user_item(ratings)

    dense_matrix = matrix.toarray()

    dense_matrix[dense_matrix == 0] = np.nan

    return pd.DataFrame(dense_matrix,index=user_id,columns=movie_id)


# Get the K similar users from the static user-user corr matrix
# K between 20 and 50 is usually good
def get_k_similar_users(correlation_matrix : pd.DataFrame, user : int, K = 30) -> pd.DataFrame:

    matrix = (correlation_matrix.loc[user].sort_values(ascending=False)[:K]).to_frame()
    
    matrix.index = matrix.index.astype(int)
    return matrix.T

# Get the K similar users from the dense user-items matrix directly (so it can be modified)
# K between 20 and 50 is usually good
# Quite fast so can be used freely
def get_k_dynamic_similar_users(user_item_matrix: pd.DataFrame, user : int, K = 30) -> pd.DataFrame:

    correlation = user_item_matrix.corrwith(user_item_matrix.loc[user],method="pearson",axis=1)

    #remove the correlation at one (either with itself or if suddenly one doesn't have any ratings anymore -> corr of one)
    correlation[correlation >= 0.99] = 0
    top = correlation.nlargest(K)
    return top.to_frame(name= user).transpose()



#####################################
# Popularity of users
#####################################



# Get the popularity factor of each users
# Formula: # list followers / # lists created
# Normalized with the min/max norm to have values between 0 and 1

# WARNING: need the user_item matrix to compare and add the missing users
# (Users with a popularity of 0 because they didn't create any list)
def get_popularity(lists : pd.DataFrame, user_item_matrix : pd.DataFrame) -> pd.DataFrame:

    nbr_follower = lists.groupby("user_id")["list_followers"].sum()
    nbr_lists = lists.groupby("user_id")["list_followers"].count()

    average = nbr_follower/nbr_lists
    average.index.name = None


    #Add missing users
    diff = user_item_matrix.index.difference(average.index)

    for index in diff:
        average[index] = 0
    
    average.sort_index(inplace=True)

    popularity = average.to_frame(name="popularity")

    return popularity


# Given the general popularity matrix and a DataFrame of K similar users, return the equivalent popularity
def get_k_popularity(popularity : pd.DataFrame, k_similar : pd.DataFrame) -> pd.DataFrame:

    k_popu = popularity.loc[k_similar.columns.values.tolist()]

    # Normalize only across the neighboorhod
    # So our most popular friend will always be 1, even if really low in the general setting

    norm_popu = ((k_popu-k_popu.min())/(k_popu.max()-k_popu.min())).fillna(0)


    return norm_popu.transpose()


# Given the general popularity matrix, return the K most popular user, with their popularity normalized
def get_top_k_popularity(popularity : pd.DataFrame, K : int) -> pd.DataFrame:

    k_popu = popularity.nlargest(K,"popularity")

    # Normalize only across the neighboorhod
    # So our most popular friend will always be 1, even if really low in the general setting

    norm_popu = ((k_popu-k_popu.min())/(k_popu.max()-k_popu.min())).fillna(0)


    return norm_popu.transpose()


#####################################
# Recommendation 
#####################################


# cf page 307, formula 9.56 mainly

# weights is the equivalent of sim(u,v), it can be the result obtained by 
# - Classical RS: get_k_similar_users
# - Popularity based RS: get_k_popularity
# - Hybrid RS: a combinaison of both output

#Having the user on the row and movies on the columns was probably a mistake...

# Sum above the division
def sum_up_norm(item : int, weights : pd.DataFrame,user_item_matrix : pd.DataFrame, average_ratings : pd.Series) -> int:
    
    sum = 0
    
    for neighboor in weights.columns:

        if not np.isnan(user_item_matrix.loc[neighboor,item]):
            
            sum += weights.loc[:,neighboor].item() * (user_item_matrix.loc[neighboor,item] - average_ratings.loc[neighboor])

    return sum



# Sum below the division
def sum_down_norm(item : int, weights : pd.DataFrame,user_item_matrix : pd.DataFrame) -> int:
    
    sum = 0
    
    for neighboor in weights.columns:
        if not np.isnan(user_item_matrix.loc[neighboor,item]):
            
            sum += weights.loc[:,neighboor].item()

    return sum

# Fill one cell of the user_item_matrix, the prediction for one user-item pair
def predict_value_norm(user : int, item : int, weights : pd.DataFrame, user_item_matrix : pd.DataFrame, average_ratings : pd.Series) -> int:

    average_user = average_ratings.loc[user]

    top = sum_up_norm(item,weights,user_item_matrix,average_ratings)

    bottom = sum_down_norm(item,weights,user_item_matrix)

    pred = (average_user + (top/bottom)) if abs(bottom) > 0.00001 else np.nan
    
    if np.isnan(pred):

        #print("Warning: no prediction possible, try to increase K to have more overlap")
        return average_user

    else: 
        
        return np.clip(pred,0,5)

#### Now the formula without normalization

# Sum above the division
def sum_up(item : int, weights : pd.DataFrame,user_item_matrix : pd.DataFrame, average_ratings : pd.Series) -> int:
    
    sum = 0
    
    for neighboor in weights.columns:

        if not np.isnan(user_item_matrix.loc[neighboor,item]):
            
            sum += weights.loc[:,neighboor].item() * (user_item_matrix.loc[neighboor,item])

    return sum



# Same sum below the division
def sum_down(item : int, weights : pd.DataFrame,user_item_matrix : pd.DataFrame) -> int:
    
    sum = 0
    
    for neighboor in weights.columns:
        if not np.isnan(user_item_matrix.loc[neighboor,item]):
            
            sum += weights.loc[:,neighboor].item()

    return sum

# Fill one cell of the user_item_matrix, the prediction for one user-item pair
def predict_value(user : int, item : int, weights : pd.DataFrame, user_item_matrix : pd.DataFrame, average_ratings : pd.Series) -> int:

    average_user = average_ratings.loc[user]

    top = sum_up(item,weights,user_item_matrix,average_ratings)

    bottom = sum_down(item,weights,user_item_matrix)

    pred = top/bottom if abs(bottom) > 0.00001 else np.nan
    
    if np.isnan(pred):

        #print("Warning: no prediction possible, try to increase K to have more overlap")
        return average_user

    else: 
        
        return np.clip(pred,0,5)

# Return the prediction for all the missing movie for a given user

# TODO: main bottleneck so far, to improve


def predict_all(user : int, weights : pd.DataFrame, user_item_matrix : pd.DataFrame, average_ratings : pd.Series, norm : boolean) -> np.array:

    #iterate over all missing ratings for a user, and for each, compute the prediction
    prediction = []

    #Only predict movies when at least 5 users in the neighboorhod gave a ratings

    missing_ratings = user_item_matrix.loc[weights.columns.values].isna().sum()

    possible_index = missing_ratings[missing_ratings <= (weights.shape[1] - 5)]

    for movie in tqdm(possible_index.index.values):
        
        if np.isnan(user_item_matrix.loc[user,movie]):

            if norm:
                prediction.append([movie,predict_value_norm(user,movie,weights,user_item_matrix,average_ratings)])
            else:
                prediction.append([movie,predict_value(user,movie,weights,user_item_matrix,average_ratings)])
            
    return np.array(prediction)


############################

# TODO I get higher ratings than 5, check why/how

############################

 


# Classic RS, the weights only considere the similarity between users
# Can chose the normalized or not normalized formula
def classic_RS(user : int, user_item_matrix : pd.DataFrame, neighboor_size = 50, top_K = 5,norm = False) -> np.array:

    similarity = get_k_dynamic_similar_users(user_item_matrix,user,neighboor_size)
    
    weights = similarity

    average_ratings = compute_average_ratings(user_item_matrix)

    all_pred = predict_all(user,weights,user_item_matrix,average_ratings,norm)

    pred = pd.DataFrame(all_pred[:,1],index=all_pred[:,0])
    
    recommendation = pred.nlargest(top_K,columns=0)
    
    recommendation.rename(columns={0:"prediction"},inplace=True)
    recommendation.index = recommendation.index.astype(int)

    return recommendation


# Popularity RS, the weights only considere the popularity of the similar users

def popularity_RS(user : int, user_item_matrix : pd.DataFrame, popu_matrix : pd.DataFrame, neighboor_size = 50, top_K = 5,norm = False) -> np.array:

    
    similarity = get_k_dynamic_similar_users(user_item_matrix,user,neighboor_size)
    popularity = get_k_popularity(popu_matrix,similarity)
    
    weights = popularity

    average_ratings = compute_average_ratings(user_item_matrix)

    all_pred = predict_all(user,weights,user_item_matrix,average_ratings,norm)

    pred = pd.DataFrame(all_pred[:,1],index=all_pred[:,0])
    
    recommendation = pred.nlargest(top_K,columns=0)
    
    recommendation.rename(columns={0:"prediction"},inplace=True)
    recommendation.index = recommendation.index.astype(int)

    return recommendation

# Hybrid RS , the weights are the sum of both the users popularity and similarity

def hybdrid_RS(user : int, user_item_matrix : pd.DataFrame, popu_matrix : pd.DataFrame, neighboor_size = 50, top_K = 5,norm = False) -> np.array:

    
    similarity = get_k_dynamic_similar_users(user_item_matrix,user,neighboor_size)
    popularity = get_k_popularity(popu_matrix,similarity)
    
    hybdrid = similarity.loc[user] + popularity.loc["popularity"]
    
    weights = hybdrid.to_frame().transpose()

    average_ratings = compute_average_ratings(user_item_matrix)

    all_pred = predict_all(user,weights,user_item_matrix,average_ratings,norm)

    pred = pd.DataFrame(all_pred[:,1],index=all_pred[:,0])
    
    recommendation = pred.nlargest(top_K,columns=0)
    
    recommendation.rename(columns={0:"prediction"},inplace=True)
    recommendation.index = recommendation.index.astype(int)

    return recommendation


# "Trending now" get a recommendation for a user based on the most popular peoples only (the same for all users)
def trending_RS(user : int, user_item_matrix : pd.DataFrame, popu_matrix : pd.DataFrame, neighboor_size = 50, top_K = 5,norm = False) -> np.array:

    
    popularity = get_top_k_popularity(popu_matrix,neighboor_size)
    
    weights = popularity

    average_ratings = compute_average_ratings(user_item_matrix)

    all_pred = predict_all(user,weights,user_item_matrix,average_ratings,norm)

    pred = pd.DataFrame(all_pred[:,1],index=all_pred[:,0])
    
    recommendation = pred.nlargest(top_K,columns=0)
    
    recommendation.rename(columns={0:"prediction"},inplace=True)
    recommendation.index = recommendation.index.astype(int)

    return recommendation