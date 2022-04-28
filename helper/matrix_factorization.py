import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm




# PROBLEM: Sometime, U and V starts containing NaN after a while... No idea why


def matrix_factorization(R, K=10, alpha=0.002, lambda_=0.02, max_iter=500):
    """
    :param R: user(row)-item(column) matrix. R similar to UxV^T
    :param K: number of features
    :param max_iter: number of iterations
    :param alpha: learning rate
    :param lambda_: regularization term for U and V
    :return: feature matrices U and V
    """

    nrows = R.shape[0]  # number of rows (users)
    ncolumns = R.shape[1]  # number of columns (items)

    # Randomly initialize U and V
    U = np.random.rand(nrows, K)
    V = np.random.rand(ncolumns, K)


    # Keep track of the avg error
    errors = []

    # Get indices of elements
    indices_full = R.nonzero()

    # Consider only a part
    # start = np.random.randint(len(indices[0]) - 1000)
    # indices = [indices[0][start:start+1000], indices[1][start:start+1000]]


    nb_batch = 10000

    for current_iter in range(max_iter):
        start = np.random.randint(len(indices_full[0]) - nb_batch)
        indices = [indices_full[0][start:start+nb_batch], indices_full[1][start:start+nb_batch]]
        for i,j in tqdm(zip(indices[0], indices[1])):
            for k in range(K):
                # Computing the partial derivative w.r.t. U
                dU = -(R[i,j] - np.sum([U[i,k] * V[j,k] for k in range(K)]))*V[j,k] + lambda_*U[i,k]
                # Computing the partial derivative w.r.t. V
                dV = -(R[i,j] - np.sum([U[i,k] * V[j,k] for k in range(K)]))*U[i,k] + lambda_*V[j,k]
                # Update U
                U[i,k] -=  alpha * dU
                # Update V
                V[j,k] -= alpha * dV


        error = 0
        for i,j in tqdm(zip(indices[0], indices[1])):
            error += 0.5*(R[i,j] - np.dot(U[i,:], V[j,:].T))**2  + np.linalg.norm(U)*(lambda_/2) + np.linalg.norm(V)*(lambda_/2)

        print(error)
        average_error = error / len(indices[0])
        print(average_error)
        errors.append(average_error)


    # Plot error evolution
    plt.plot(range(len(errors)), errors, label='Error')
    plt.title('Average error evolution')
    plt.xlabel('Iterations')
    plt.ylabel('Average error')
    plt.legend()
    plt.show()

    # return
    return U, V
