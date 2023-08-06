import numpy as np
from scipy.linalg import solve_triangular, cho_factor, cho_solve

from gpatom.gpfp.kernel import FPKernel, FPKernelParallel, FPKernelNoforces
from gpatom.gpfp.prior import ConstantPrior


class GaussianProcess:

    '''Gaussian Process Regression
    It is recomended to be used with other Priors and Kernels
    from ase.optimize.gpmin

    Parameters:

    prior: Prior class, as in ase.optimize.gpmin.prior
        Defaults to ZeroPrior

    kernel: Kernel function for the regression, as
       in ase.optimize.gpmin.kernel
        Defaults to the Squared Exponential kernel with derivatives '''

    def __init__(self, hp={}, prior=None, kerneltype='sqexp',
                 use_forces=True, parallelkernel=True):

        default_params = dict(scale=1,
                              weight=1,
                              noise=1e-3,
                              noisefactor=0.5)
        default_params.update({'ratio': default_params['noise'] /
                               default_params['weight']})

        self.hp = default_params  # hyperparameters in dictionary
        self.use_forces = use_forces

        if self.use_forces:
            if parallelkernel:
                self.kernel = FPKernelParallel(kerneltype)
            else:
                self.kernel = FPKernel(kerneltype)
        else:
            self.kernel = FPKernelNoforces(kerneltype)

        if prior is None:
            prior = ConstantPrior(0.0)
        self.prior = prior
        self.prior.use_forces = self.use_forces

        self.set_hyperparams(hp)

    def set_hyperparams(self, new_params):

        self.hp.update(new_params)

        if 'ratio' not in self.hp:
            ratio = self.hp['noise'] / self.hp['weight']
            self.set_ratio(ratio)

        # Keep noise-weight ratio as constant:
        self.hp['noise'] = self.hp['ratio'] * self.hp['weight']

        if 'prior' in self.hp.keys():
            self.prior.set_constant(self.hp['prior'])

        self.kernel.set_params(self.hp)

        return self.hp

    def train(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        K = self.kernel.kernel_matrix(X)

        self.X = X
        self.Y = Y

        Natoms = int((len(self.Y.flatten()) / len(self.X) - 1) / 3)
        self.K = self.add_regularization(K, Ntrain=len(self.X), Natoms=Natoms)
        self.model_vector = self.calculate_model_vector(K)

        return

    def add_regularization(self, matrix, Ntrain, Natoms):

        if self.use_forces:
            D = Natoms * 3  # number of derivatives
            regularization = np.array(Ntrain * ([self.hp['noise'] *
                                                 self.hp['noisefactor']] +
                                                D * [self.hp['noise']]))

        else:
            regularization = np.array(Ntrain * ([self.hp['noise'] *
                                                 self.hp['noisefactor']]))

        matrix += np.diag(regularization**2)
        return matrix

    def calculate_model_vector(self, matrix):

        # factorize K-matrix:
        self.L, self.lower = cho_factor(matrix,
                                        lower=True,
                                        check_finite=True)

        # Update the prior if it is allowed to update:
        if self.prior.use_update:
            self.prior.update(self.X, self.Y, self.L)

        self.prior_array = self.calculate_prior_array(self.X)
        model_vector = self.Y.flatten() - self.prior_array

        # Overwrite model vector so that it becomes C^-1 * (Y - prior):
        cho_solve((self.L, self.lower), model_vector,
                  overwrite_b=True, check_finite=True)
        return model_vector

    def calculate_prior_array(self, list_of_fingerprints):
        return list(np.hstack([self.prior.prior(x)
                               for x in list_of_fingerprints]))

    def predict(self, x, get_variance=False):
        '''
        If get_variance==False, then variance
        is returned as None
        '''

        k = self.kernel.kernel_vector(x, self.X)

        prior_array = self.calculate_prior_array([x])
        f = prior_array + np.dot(k, self.model_vector)

        if not self.use_forces:
            x.recalculate(calc_gradients=True)

            dk_dxi = (self.hp['weight']**2 *
                      np.array([self.kernel.kerneltype.kernel_gradient(x, x2)
                                for x2 in self.X]))

            forces = np.einsum('ijk,i->jk', dk_dxi,
                               self.model_vector).flatten()

            f = list(f) + list(forces)
            f = np.array(f)

        V = self.calculate_variance(get_variance, k, x)

        return f, V

    def calculate_variance(self, get_variance, k, x):
        V = None
        if get_variance:
            k_transpose = k.T.copy()
            k_transpose = solve_triangular(self.L,
                                           k_transpose,
                                           lower=True,
                                           check_finite=False)

            variance = self.kernel.kernel(x, x)
            covariance = np.tensordot(k_transpose, k_transpose,
                                      axes=(0, 0))

            V = variance - covariance
        return V

    def logP(self):
        y = self.Y.flatten()
        logP = (- 0.5 * np.dot(y - self.prior_array, self.model_vector)
                - np.sum(np.log(np.diag(self.L)))
                - len(y) / 2 * np.log(2 * np.pi))

        return logP
