from helper.loader import load_ratings, load_movies, load_lists
from helper.preprocesser import preprocess_ratings
import helper.collaborative as coll
from scipy.sparse import csr_matrix
from helper.preprocesser import prepare_test_data_dense, prepare_test_data_sparse
from helper.matrix_factorization_faster import matrix_factorization
import pandas as pd
import numpy as np
import argparse
import time


def main(args):
    # Load data
    ratings = load_ratings()
    lists = load_lists()
    print('Data loaded')

    # Reduce data
    ratings_new, lists_new = preprocess_ratings(ratings, lists, min_ratings_user = 500, min_ratings_movie = 500)
    print('Data reduced')


    # Get (sparse) matrix
    sparse_user_item, u_list, i_list = coll.get_sparse_user_item(ratings_new)
    print('User-Item matrix created')


    K = int(args.K)
    alpha = args.alpha
    lambda_ = args.lambda_
    max_iter = int(args.max_iter)
    nb_batch = args.batch_size if args.batch_size > 0 else 'all'
    plot_name = args.plot_name
    save_results = True if args.save_results == 'True' else False
    checkpoints_each = args.checkpoints_each

    # Factorize (or try at least..) matrix
    start = time.time()
    matrix_factorization(R=sparse_user_item, K=K, alpha=alpha, lambda_=lambda_, max_iter=max_iter, nb_batch=nb_batch, plot_name=plot_name, save_results=save_results, checkpoints_each=checkpoints_each, u_list=u_list, i_list=i_list)
    print(f'factorization time: {time.time() - start}')


if __name__ == "__main__":
    # Ev. extract parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--K', type=float, default=5, help='The number of feature for each user/item')
    parser.add_argument('--alpha', type=float, default=0.002, help='The learning rate')
    parser.add_argument('--lambda_', type=float, default=0.02, help='Parameters for the partial derivatives')
    parser.add_argument('--max_iter', type=int, default=10, help='Number of epochs')
    parser.add_argument('--batch_size', type=int, default=10000, help='Number of items to consider for each epoch. Use -1 for all')
    parser.add_argument('--plot_name', type=str, default='fig.png', help='Name of the file with the error evolution')
    parser.add_argument('--save_results', type=str, default='True', help='Whether to save U and V on file')
    parser.add_argument('--checkpoints_each', type=int, default=None, help='After how many epochs write a checkpoint. By default, do not write any')
    args = parser.parse_args()
    main(args)
