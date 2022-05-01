import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool



def K_loop(R, U, V):
    pass





def matrix_factorization(R, K=10, alpha=0.002, lambda_=0.02, max_iter='all', nb_batch=100000, plot_name='fig.png', save_results=False):
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


    # Plot error evolution
    plt.plot(range(len(errors)), errors, label='Error')
    plt.title('Average error evolution')
    plt.xlabel('Iterations')
    plt.ylabel('Average error')
    plt.legend()
    plt.savefig(plot_name)

    if save_results:
        np.save('U.npy', U)
        np.save('V.npy', V)

    # return
    return U, V
