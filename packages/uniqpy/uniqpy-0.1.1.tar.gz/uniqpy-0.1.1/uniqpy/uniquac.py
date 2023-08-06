from scipy.spatial.distance import euclidean, braycurtis
import numpy as np


def get_U_mat(string, N):
    mat = np.zeros((N, N))

    current_len = N
    current_shift = 0

    while current_len != 0:
        line = string[current_shift:current_shift + current_len]
        mat[N-current_len][N-current_len:] = line

        current_shift += current_len
        current_len -= 1

    for i in range(0, len(mat)):
        for j in range(i, len(mat)):
            mat[j][i] = mat[i][j]
    
    return mat


def get_tau_mat(U_mat):

    tau_mat = np.zeros(U_mat.shape)

    for i in range(len(U_mat)):
        for j in range(len(U_mat)):
            tau_mat[i][j] = U_mat[i][i]/U_mat[i][j]
    return tau_mat


def get_l_term(r, q, z):

    return (z/2)*(r-q) - (r-1)

def get_combinatorial_term(
        x, r, q, z=10
        ):
    V = x*r/np.sum(x*r)
    F = x*q/np.sum(x*q)
    l = get_l_term(r, q, z)

    
    
    result = np.log(V/x) + (z/2) * q * np.log(F/V) + l - (V/x)*np.sum(x*l)
    return result

def get_residual_term(
        x, r, q, tau):
    V = x*r/np.sum(x*r)
    F = x*q/np.sum(x*q)

    result = np.ones(len(x))
    for i in range(len(x)):
        result[i] -= np.log(np.sum(F*tau.T[i]))

        for j in range(len(x)):
            result[i] -= F[j]*tau[i][j]/np.sum(F*tau.T[j])

    result *= q

    return result


def get_coefs(x, q, r, tau, z=10):
    combinatorial_term = get_combinatorial_term(x, r, q, z=z)

    residual_term = get_residual_term(x, r, q, tau)

    result = combinatorial_term + residual_term

    
    
    return np.exp(result)


def parse_coefs(K, N):
    return get_tau_mat(get_U_mat(K, N))


def get_concetrations(x, coefs):

    return x*coefs/np.sum(x*coefs)


def get_sample_error(x, y, coefs):
    
    return braycurtis(
        y, get_concetrations(x, coefs)
    )


def get_dataset_error(K, X, Y, R, Q):

    N = X.shape[1]

    parameters = R, Q, parse_coefs(K, N)
    error = 0

    for i in range(len(X)):
        x, y = X[i], Y[i]
        coefs = get_coefs(x, *parameters)
        error += get_sample_error(x, y, coefs)

    error /= X.shape[0]

    return error


def get_error_by_X(x, y, K, R, Q):

    N = x.shape[0]

    parameters = R, Q, parse_coefs(K, N)
    coefs = get_coefs(x, *parameters)

    error = get_sample_error(x, y, coefs)
    return error


def optimizeX (K, y, R, Q):

    initial_X = np.ones(len(y))

    results = minimize(
        get_error_by_X,
        initial_X,
        args=(y, K, R, Q),
        tol=0.00000001,
        method='SLSQP'
        )

    return results.x/np.sum(results.x)


def predict_dataset(X, E, R, Q):

    parameters = R, Q, parse_coefs(E, X.shape[1])

    pred_y = np.zeros(X.shape)

    for i in range(len(X)):
        x = X[i]

        coefs = get_coefs(x, *parameters)
        pred_y[i] = get_concetrations(x, coefs)

    return pred_y




from scipy.optimize import minimize

def fit_UNIQUAC_model(x, y, R, Q):

    x = np.array(x)
    y = np.array(y)

    N = x.shape[1]

    initial_K = np.ones(int((N*(N + 1)/2)))

    results = minimize(
        get_dataset_error,
        initial_K,
        args=(x, y, R, Q),
        tol=0.00001,
        method='SLSQP',
        options={'maxiter': 1000, 'disp': False}
    )


    best_parameters = results.x

    return best_parameters
    
