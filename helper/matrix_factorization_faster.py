import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time
import os
from datetime import datetime
import pandas as pd


def matrix_factorization_precomputed(user, top_K=10):
    # Load U and V matrix
    U = np.load('data/MatrixFactorization/U_20.npy')
    V = np.load('data/MatrixFactorization/V_20.npy')

    # Load reference to users and items (movies)
    u_list = np.load('data/MatrixFactorization/u_list.npy')
    i_list = np.load('data/MatrixFactorization/i_list.npy')

    # Get index of user
    user_index = u_list.tolist().index(user)
    # print(user)
    # print(user_index)
    # print(u_list)

    if user_index is None:
        print('User not in matrix database')
        return []

    # Predict values
    predictions = U[user_index,:].dot(V.T)

    # Get index (in UxVt) of bests
    recommendation = pd.DataFrame(predictions).nlargest(top_K, columns=0)
    index_largest = recommendation.index

    # Retrive original indices
    indices = []
    for i in index_largest:
        # if not i_list[i] in list(m.loc[:,'movie_id']):
        #      print(f'm does not contain {i_list[i]}')
        # else:
        #     print(f'm contains {i_list[i]}!')
        indices.append(i_list[i])

    # Uniform pandas df
    recommendation.rename(columns={0:"prediction"},inplace=True)
    recommendation.index = indices
    recommendation.index = recommendation.index.astype(int)

    return recommendation


def matrix_factorization(R, K=10, alpha=0.002, lambda_=0.02, max_iter='all', nb_batch=100000, plot_name='fig.png', save_results=False, checkpoints_each=None, u_list=None, i_list=None):
    """
    :param R: user(row)-item(column) matrix. R similar to UxV^T
    :param K: number of features
    :param max_iter: number of iterations
    :param alpha: learning rate
    :param lambda_: regularization term for U and V
    :return: feature matrices U and V
    """

    # Record time used
    start_time = time.time()

    nrows = R.shape[0]  # number of rows (users)
    ncolumns = R.shape[1]  # number of columns (items)

    # Randomly initialize U and V
    U = np.random.rand(nrows, K)
    V = np.random.rand(ncolumns, K)


    # Keep track of the avg error
    errors = []

    # Get indices of elements
    indices_full = R.nonzero()

    # Create chekcpoints folder
    if checkpoints_each is not None or save_results:
        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Create outer folder
        if not os.path.exists('checkpoints'):
            os.makedirs('checkpoints')
        # Create a unique name for the checkpoints
        date_and_time = date_and_time.replace(" ", "__")
        date_and_time = date_and_time.replace(":", "-")
        date_and_time = date_and_time.replace("/", "-")
        date_and_time = date_and_time.replace(".", "-")
        checkpoints_folder = f'checkpoints/{date_and_time}'
        print(checkpoints_folder)
        # Create execution folder
        if not os.path.exists(checkpoints_folder):
            os.makedirs(checkpoints_folder)

        # Save user list and item list
        if checkpoints_each is not None:
            if u_list is not None: np.save(f'{checkpoints_folder}/u_list.npy', u_list)
            if i_list is not None: np.save(f'{checkpoints_folder}/i_list.npy', i_list)


    def update(i, j):
        if not np.isnan(R[i,j]):
            for k in range(K):
                # Computing the partial derivative w.r.t. U
                dot = U[i].dot(V[j].T)
                dU = -(R[i,j] - dot)*V[j,k] + lambda_*U[i,k]
                # Computing the partial derivative w.r.t. V
                dV = -(R[i,j] - dot)*U[i,k] + lambda_*V[j,k]
                # Update U
                U[i,k] -= alpha * dU
                # Update V
                V[j,k] -= alpha * dV


    def evaluate(i, j):
        if not np.isnan(R[i,j]):
            return 0.5*(R[i,j] - np.dot(U[i], V[j].T))**2  + np.linalg.norm(U)*(lambda_/2) + np.linalg.norm(V)*(lambda_/2)
        else:
            return 0


    # Vectorize function (but no big improvement in performance)
    vu = np.vectorize(update)
    ve = np.vectorize(evaluate)

    for current_iter in range(max_iter):
        if nb_batch != 'all':
            # Consider only a part
            start = np.random.randint(len(indices_full[0]) - nb_batch)
            indices = [indices_full[0][start:start+nb_batch], indices_full[1][start:start+nb_batch]]
        else:
            indices = indices_full

        # Update
        vu(indices[0], indices[1])

        # Evaluate
        error = ve(indices[0], indices[1]).sum()

        average_error = error / len(indices[0])
        print(f"Avg. error: {round(average_error, 5)} (it {current_iter+1}/{max_iter})")
        errors.append(average_error)

        if checkpoints_each is not None and ((current_iter + 1) % checkpoints_each == 0):
            np.save(f'{checkpoints_folder}/U_{current_iter + 1}.npy', U)
            np.save(f'{checkpoints_folder}/V_{current_iter + 1}.npy', V)


    execution_time = round(time.time() - start_time, 2)

    # Plot error evolution
    plt.plot(range(len(errors)), errors, label='Error')
    plt.title(f'Average error evolution (time: {execution_time} seconds)')
    plt.xlabel('Iterations')
    plt.ylabel('Average error')
    plt.legend()
    plt.savefig(f'{checkpoints_folder}/{plot_name}')

    if save_results:
        # Save matrices
        np.save(f'{checkpoints_folder}/U.npy', U)
        np.save(f'{checkpoints_folder}/V.npy', V)
        # Save parameters
        lines = [f'K = {K}\n',
                 f'Alpha = {alpha}\n',
                 f'Lambda = {lambda_}\n',
                 f'Max_iter = {max_iter}\n',
                 f'Nb_batch = {nb_batch}\n',
                 f'Execution time = {execution_time} seconds']
        with open(f'{checkpoints_folder}/parameters.txt', 'w') as f:
            f.writelines(lines)

    # return
    return U, V
