import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

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
    indices = R.nonzero()

    # Consider only a part
    start = np.random.randint(len(indices[0]) - 1000)
    indices = [indices[0][start:start+1000], indices[1][start:start+1000]]

    iterator = zip(indices[0], indices[1])

    for current_iter in range(max_iter):
        for i,j in tqdm(iterator):
            for k in range(K):
                # Computing the partial derivative w.r.t. U
                dU = -(R[i,j] - np.sum([U[i,k] * V[j,k] for k in range(K)]))*V[j,k] + lambda_*U[i,k]
                # Computing the partial derivative w.r.t. V
                dV = -(R[i,j] - np.sum([U[i,k] * V[j,k] for k in range(K)]))*U[i,k] + lambda_*V[j,k]
                # Update U
                U[i,k] -=  alpha * dU
                # Update V
                V[j,k] -= alpha * dV

        # print('out of first loop')
        error = 0
        counter = 0
        print('before transpose')
        # print('after transpose')
        print('before second loop')
        for i,j in tqdm(zip(indices[0], indices[1])):
            print('in second loop')
            error += 0.5*(R[i,j] - np.dot(U, V.T)[i,j])**2  + np.linalg.norm(U)*(lambda_/2) + np.linalg.norm(V)*(lambda_/2)
            counter = counter + 1
        print('after second loop')

        average_error = error / counter
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


        #
        # for i in range(nrows):  # R rows iterator
        #     for j in range(ncolumns):  # R column iterator
        #         if R[i][j] > 0:  # indicator function
        #             # Block update  -> no big difference
        #             # new_u = []
        #             # new_v = []
        #             for k in range(K):
        #                 # Computing the partial derivative w.r.t. U
        #                 dU = -(R[i,j] - numpy.sum([U[i,k] * V[j,k] for k in range(K)]))*V[j,k] + lambda_*U[i,k]
        #                 # dU = 0
        #                 # Computing the partial derivative w.r.t. V
        #         # !!! In the slides the first '-' is missing, which causes the algorithm to oscillate around a certain value (or to diverge, if updating only V)
        #                 dV = -(R[i,j] - numpy.sum([U[i,k] * V[j,k] for k in range(K)]))*U[i,k] + lambda_*V[j,k]
        #                 # Update U
        #                 # new_u.append(U[i,k] - alpha * dU)
        #                 U[i,k] -=  alpha * dU
        #                 # Update V
        #                 # new_v.append(V[j,k] - alpha * dV)
        #                 V[j,k] -= alpha * dV
        #             # Block update
        #             # U[i,:] = new_u
        #             # V[j,:] = new_v
        #
        # error = 0
        # counter = 0
        # for i in range(nrows):
        #     for j in range(ncolumns):
        #         if R[i][j] > 0:
        #             # compute the overall error (objective loss function)
        #             # error += numpy.linalg.norm(R[i,j] - numpy.dot(U, V.T)[i,j])/2 + numpy.linalg.norm(U)*(lambda_/2) + numpy.linalg.norm(V)*(lambda_/2)
        #             error += 0.5*(R[i,j] - numpy.dot(U, V.T)[i,j])**2  + numpy.linalg.norm(U)*(lambda_/2) + numpy.linalg.norm(V)*(lambda_/2)
        #             counter = counter + 1
        #
        # average_error = error / counter
        # print(f"{current_iter + 1} iteration: average error {average_error}")
        # errors.append(average_error)
        #
        # # Stop criteria
        # if average_error < 0.15:
        #     break
    #
    # # Plot error evolution
    # plt.plot(range(len(errors)), errors, label='Error')
    # plt.title('Average error evolution')
    # plt.xlabel('Iterations')
    # plt.ylabel('Average error')
    # plt.legend()
    # plt.show()
    #
    # # return
    # return U, V
