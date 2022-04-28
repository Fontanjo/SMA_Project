from helper.loader import load_ratings, load_movies, load_lists
from helper.preprocesser import preprocess_ratings, more_than_N_ratings, create_fake_identities
import helper.network_explorer as ne
import helper.collaborative as coll
from scipy.sparse import csr_matrix
from helper.preprocesser import prepare_test_data_dense, prepare_test_data_sparse
from helper.matrix_factorization import matrix_factorization
import pandas as pd
import numpy as np






def main():
    # Load data
    ratings = load_ratings()
    lists = load_lists()

    # Reduce data
    ratings_new, lists_new = preprocess_ratings(ratings, lists, min_ratings = 500)
    
    # Get (sparse) matrix
    sparse_user_item, _, _ = coll.get_sparse_user_item(ratings_new)
    
    # Factorize (or try at least..) matrix
    matrix_factorization(R=sparse_user_item, K=5, alpha=0.002, lambda_=0.02, max_iter=5)







if __name__ == "__main__":
    main()
